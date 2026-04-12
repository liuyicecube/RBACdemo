"""Operation Log Service"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from App.Models.OperationLog import OperationLogModel
from App.Repositories.OperationLogRepository import OperationLogRepository
from App.Schemas.OperationLog import OperationLogCreate
from App.Core.Exceptions import NotFoundException
import json
import hashlib


class OperationLogService:
    """操作日志服务类"""

    def __init__(self, db: Session):
        """初始化操作日志服务"""
        self.db = db
        self.operation_log_repository = OperationLogRepository(db)

    def get_log_by_id(self, log_id: int, tenant_id: Optional[int] = None) -> OperationLogModel:
        """根据ID获取日志"""
        log = self.operation_log_repository.get_by_id(log_id, tenant_id=tenant_id)
        if not log:
            raise NotFoundException(detail="日志不存在")
        return log

    def create_log(self, log_create: OperationLogCreate, tenant_id: int) -> OperationLogModel:
        """创建日志"""
        log = OperationLogModel(
            tenant_id=tenant_id,
            user_id=log_create.user_id,
            username=log_create.username,
            module=log_create.module,
            operation=log_create.operation,
            request_method=log_create.method,
            request_url=log_create.url,
            ip_address=log_create.ip,
            request_params=log_create.params,
            response_result=log_create.result,
            status=log_create.status or 1,
            error_message=log_create.error_msg,
            execution_time=log_create.execution_time
        )

        return self.operation_log_repository.create(log)

    def get_logs_by_user(self, user_id: int, tenant_id: int, page: int = 1, page_size: int = 20) -> Tuple[int, List[OperationLogModel]]:
        """根据用户获取日志"""
        query = self.db.query(OperationLogModel).filter(
            OperationLogModel.user_id == user_id,
            OperationLogModel.tenant_id == tenant_id
        )

        total = query.count()
        items = query.order_by(OperationLogModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return total, items

    def paginate_logs(
        self,
        tenant_id: int,
        keyword: str = None,
        module: str = None,
        user_id: int = None,
        status: int = None,
        start_time: datetime = None,
        end_time: datetime = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[OperationLogModel]]:
        """分页查询日志"""
        return self.operation_log_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            module=module,
            user_id=user_id,
            status=status,
            start_time=start_time,
            end_time=end_time,
            page=page,
            page_size=page_size
        )

    def delete_old_logs(self, days: int, tenant_id: int):
        """删除旧日志"""
        self.operation_log_repository.delete_old_logs(days, tenant_id)

    def get_statistics(self, tenant_id: int, days: int = 7) -> dict:
        """获取统计数据"""
        from datetime import datetime, timedelta
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        total_logs = self.db.query(OperationLogModel).filter(
            OperationLogModel.tenant_id == tenant_id,
            OperationLogModel.create_time >= start_time,
            OperationLogModel.create_time <= end_time
        ).count()

        success_logs = self.db.query(OperationLogModel).filter(
            OperationLogModel.tenant_id == tenant_id,
            OperationLogModel.status == 1,
            OperationLogModel.create_time >= start_time,
            OperationLogModel.create_time <= end_time
        ).count()

        failed_logs = total_logs - success_logs

        return {
            "total_logs": total_logs,
            "success_logs": success_logs,
            "failed_logs": failed_logs,
            "success_rate": round(success_logs / total_logs * 100, 2) if total_logs > 0 else 0
        }

    def create_log_enhanced(
        self,
        tenant_id: int,
        user_id: int,
        username: str,
        module: str,
        operation: str,
        method: str,
        url: str,
        ip: str,
        params: Optional[str] = None,
        result: Optional[str] = None,
        status: int = 1,
        error_msg: Optional[str] = None,
        execution_time: Optional[int] = None,
        user_agent: Optional[str] = None,
        request_id: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ) -> OperationLogModel:
        """增强的日志创建方法，添加更多上下文信息"""
        log_params = {
            "tenant_id": tenant_id,
            "user_id": user_id,
            "username": username,
            "module": module,
            "operation": operation,
            "request_method": method,
            "request_url": url,
            "ip_address": ip,
            "request_params": self._mask_sensitive_params(params),
            "response_result": self._mask_sensitive_data(result),
            "status": status,
            "error_message": error_msg,
            "execution_time": execution_time,
            "user_agent": user_agent
        }

        if extra:
            extra_data = extra.copy()
            if request_id:
                extra_data["request_id"] = request_id
            log_params["request_params"] = json.dumps({
                "original": log_params["request_params"],
                "extra": extra_data
            }) if log_params["request_params"] else json.dumps({"extra": extra_data})

        log = OperationLogModel(**log_params)
        return self.operation_log_repository.create(log)

    def _mask_sensitive_params(self, params: Optional[str]) -> Optional[str]:
        """掩码敏感参数"""
        if not params:
            return params

        try:
            data = json.loads(params)
            if isinstance(data, dict):
                sensitive_keys = ["password", "token", "secret", "credit_card", "ssn", "phone", "email"]
                for key in data:
                    if any(sensitive in key.lower() for sensitive in sensitive_keys):
                        data[key] = "***"
                return json.dumps(data, ensure_ascii=False)
        except Exception:
            pass

        return params

    def _mask_sensitive_data(self, data: Optional[str]) -> Optional[str]:
        """掩码敏感数据"""
        if not data:
            return data

        if "password" in data.lower() or "token" in data.lower():
            return "*** 包含敏感数据已隐藏 ***"

        return data

    def get_top_modules(self, tenant_id: int, days: int = 7, limit: int = 10) -> List[Dict[str, Any]]:
        """获取热门操作模块"""
        from datetime import datetime, timedelta
        from sqlalchemy import func

        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        result = self.db.query(
            OperationLogModel.module,
            func.count(OperationLogModel.id).label("count")
        ).filter(
            OperationLogModel.tenant_id == tenant_id,
            OperationLogModel.create_time >= start_time,
            OperationLogModel.create_time <= end_time
        ).group_by(OperationLogModel.module).order_by(
            func.count(OperationLogModel.id).desc()
        ).limit(limit).all()

        return [{"module": r[0], "count": r[1]} for r in result]

    def get_user_activity(self, tenant_id: int, days: int = 7) -> List[Dict[str, Any]]:
        """获取用户活跃情况"""
        from datetime import datetime, timedelta
        from sqlalchemy import func

        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        result = self.db.query(
            OperationLogModel.username,
            func.count(OperationLogModel.id).label("count")
        ).filter(
            OperationLogModel.tenant_id == tenant_id,
            OperationLogModel.create_time >= start_time,
            OperationLogModel.create_time <= end_time
        ).group_by(OperationLogModel.username).order_by(
            func.count(OperationLogModel.id).desc()
        ).limit(20).all()

        return [{"username": r[0], "count": r[1]} for r in result]
