"""Audit Log Service"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from App.Models.AuditLog import AuditLogModel
from App.Repositories.AuditLogRepository import AuditLogRepository
from App.Schemas.AuditLog import AuditLogCreate
from App.Core.Exceptions import NotFoundException
import json
from difflib import SequenceMatcher


class AuditLogService:
    """审计日志服务类"""

    def __init__(self, db: Session):
        """初始化审计日志服务"""
        self.db = db
        self.audit_log_repository = AuditLogRepository(db)

    def get_log_by_id(self, log_id: int, tenant_id: Optional[int] = None) -> AuditLogModel:
        """根据ID获取日志"""
        log = self.audit_log_repository.get_by_id(log_id, tenant_id=tenant_id)
        if not log:
            raise NotFoundException(detail="审计日志不存在")
        return log

    def create_log(self, log_create: AuditLogCreate, tenant_id: int) -> AuditLogModel:
        """创建审计日志"""
        log = AuditLogModel(
            tenant_id=tenant_id,
            user_id=log_create.user_id,
            username=log_create.username,
            table_name=log_create.table_name,
            record_id=log_create.record_id,
            operation_type=log_create.operation_type,
            field_name=log_create.change_fields,
            old_value=log_create.old_value,
            new_value=log_create.new_value
        )

        return self.audit_log_repository.create(log)

    def get_logs_by_record(self, table_name: str, record_id: int, tenant_id: int, page: int = 1, page_size: int = 20) -> Tuple[int, List[AuditLogModel]]:
        """根据记录获取变更历史"""
        query = self.db.query(AuditLogModel).filter(
            AuditLogModel.table_name == table_name,
            AuditLogModel.record_id == record_id,
            AuditLogModel.tenant_id == tenant_id
        )

        total = query.count()
        items = query.order_by(AuditLogModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return total, items

    def paginate_logs(
        self,
        tenant_id: int,
        keyword: str = None,
        table_name: str = None,
        record_id: int = None,
        operation_type: str = None,
        user_id: int = None,
        start_time: datetime = None,
        end_time: datetime = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[AuditLogModel]]:
        """分页查询审计日志"""
        return self.audit_log_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            table_name=table_name,
            record_id=record_id,
            operation_type=operation_type,
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            page=page,
            page_size=page_size
        )

    def delete_old_logs(self, days: int, tenant_id: int):
        """删除旧日志"""
        self.audit_log_repository.delete_old_logs(days, tenant_id)

    def get_statistics(self, tenant_id: int, days: int = 7) -> dict:
        """获取统计数据"""
        from datetime import datetime, timedelta
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        total_logs = self.db.query(AuditLogModel).filter(
            AuditLogModel.tenant_id == tenant_id,
            AuditLogModel.create_time >= start_time,
            AuditLogModel.create_time <= end_time
        ).count()

        insert_logs = self.db.query(AuditLogModel).filter(
            AuditLogModel.tenant_id == tenant_id,
            AuditLogModel.operation_type == 'INSERT',
            AuditLogModel.create_time >= start_time,
            AuditLogModel.create_time <= end_time
        ).count()

        update_logs = self.db.query(AuditLogModel).filter(
            AuditLogModel.tenant_id == tenant_id,
            AuditLogModel.operation_type == 'UPDATE',
            AuditLogModel.create_time >= start_time,
            AuditLogModel.create_time <= end_time
        ).count()

        delete_logs = self.db.query(AuditLogModel).filter(
            AuditLogModel.tenant_id == tenant_id,
            AuditLogModel.operation_type == 'DELETE',
            AuditLogModel.create_time >= start_time,
            AuditLogModel.create_time <= end_time
        ).count()

        return {
            "total_logs": total_logs,
            "insert_logs": insert_logs,
            "update_logs": update_logs,
            "delete_logs": delete_logs
        }

    def compare_data(self, log_id: int, tenant_id: Optional[int] = None) -> Dict[str, Any]:
        """对比数据变更，返回详细的变更差异"""
        log = self.get_log_by_id(log_id, tenant_id=tenant_id)

        if log.operation_type != 'UPDATE':
            return {
                "log_id": log_id,
                "operation_type": log.operation_type,
                "message": "只有UPDATE操作可以进行数据对比"
            }

        old_data = self._parse_json(log.old_value)
        new_data = self._parse_json(log.new_value)

        changes = self._calculate_diff(old_data, new_data)

        return {
            "log_id": log_id,
            "table_name": log.table_name,
            "record_id": log.record_id,
            "operation_type": log.operation_type,
            "changes": changes,
            "change_count": len(changes)
        }

    def _parse_json(self, data: Optional[str]) -> Dict[str, Any]:
        """解析JSON数据"""
        if not data:
            return {}
        try:
            return json.loads(data)
        except Exception:
            return {"raw": data}

    def _calculate_diff(self, old_data: Dict[str, Any], new_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """计算两个字典之间的差异"""
        changes = []

        all_keys = set(old_data.keys()).union(set(new_data.keys()))

        for key in all_keys:
            old_value = old_data.get(key)
            new_value = new_data.get(key)

            if old_value == new_value:
                continue

            change_type = None
            if key not in old_data:
                change_type = "added"
            elif key not in new_data:
                change_type = "removed"
            else:
                change_type = "modified"

            changes.append({
                "field": key,
                "type": change_type,
                "old_value": old_value,
                "new_value": new_value,
                "similarity": self._calculate_similarity(old_value, new_value)
            })

        return sorted(changes, key=lambda x: x["field"])

    def _calculate_similarity(self, old_value: Any, new_value: Any) -> Optional[float]:
        """计算两个值的相似度"""
        if old_value is None or new_value is None:
            return None

        old_str = str(old_value)
        new_str = str(new_value)

        if not old_str and not new_str:
            return 1.0

        matcher = SequenceMatcher(None, old_str, new_str)
        return round(matcher.ratio(), 2)

    def create_log_with_diff(
        self,
        tenant_id: int,
        user_id: int,
        username: str,
        table_name: str,
        record_id: int,
        operation_type: str,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        auto_calculate_changes: bool = True
    ) -> AuditLogModel:
        """创建审计日志并自动计算变更字段"""
        change_fields = None

        if auto_calculate_changes and operation_type == 'UPDATE':
            old_data = self._parse_json(old_value)
            new_data = self._parse_json(new_value)
            diffs = self._calculate_diff(old_data, new_data)
            change_fields = json.dumps([f["field"] for f in diffs if f["type"] == "modified"], ensure_ascii=False)

        log = AuditLogModel(
            tenant_id=tenant_id,
            user_id=user_id,
            username=username,
            table_name=table_name,
            record_id=record_id,
            operation_type=operation_type,
            old_value=old_value,
            new_value=new_value,
            change_fields=change_fields
        )

        return self.audit_log_repository.create(log)

    def get_data_history(
        self,
        table_name: str,
        record_id: int,
        tenant_id: int
    ) -> List[Dict[str, Any]]:
        """获取记录的完整变更历史"""
        query = self.db.query(AuditLogModel).filter(
            AuditLogModel.table_name == table_name,
            AuditLogModel.record_id == record_id,
            AuditLogModel.tenant_id == tenant_id
        ).order_by(AuditLogModel.create_time.asc()).all()

        history = []
        current_data = {}

        for log in query:
            if log.operation_type == 'INSERT':
                current_data = self._parse_json(log.new_value)
            elif log.operation_type == 'UPDATE':
                new_data = self._parse_json(log.new_value)
                current_data.update(new_data)
            elif log.operation_type == 'DELETE':
                current_data = {}

            history.append({
                "log_id": log.id,
                "operation_type": log.operation_type,
                "create_time": log.create_time,
                "username": log.username,
                "data_snapshot": current_data.copy()
            })

        return history
