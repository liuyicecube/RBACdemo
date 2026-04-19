"""Operation Log Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
from App.Schemas.Auth import AuthResponse
from App.Services.OperationLogService import OperationLogService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Response import ResponseUtils
from App.Utils.OperationLog import OperationLogUtils


router = APIRouter(
    prefix="/operation-logs",
    tags=["操作日志管理"]
)


@router.get("", response_model=AuthResponse, summary="获取操作日志列表", dependencies=[Depends(permission_dependency("log:view"))])
def get_operation_logs(
    keyword: str = None,
    module: str = None,
    user_id: int = None,
    status: int = None,
    start_time: str = None,
    end_time: str = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取操作日志列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        log_service = OperationLogService(db)

        start_datetime = None
        end_datetime = None
        if start_time:
            start_datetime = datetime.fromisoformat(start_time)
        if end_time:
            end_datetime = datetime.fromisoformat(end_time)

        total, logs = log_service.paginate_logs(
            tenant_id=tenant_id,
            keyword=keyword,
            module=module,
            user_id=user_id,
            status=status,
            start_time=start_datetime,
            end_time=end_datetime,
            page=page,
            page_size=page_size
        )

        log_list = []
        for log in logs:
            description = log.description
            if not description and log.request_url:
                try:
                    description = OperationLogUtils.generate_description(
                        log.request_url, 
                        log.request_method or "GET", 
                        log.module or "", 
                        log.operation or ""
                    )
                except:
                    pass
            
            log_list.append({
                "id": log.id,
                "user_id": log.user_id,
                "username": log.username,
                "module": log.module,
                "operation": log.operation,
                "description": description,
                "method": log.request_method,
                "url": log.request_url,
                "ip": log.ip_address,
                "params": log.request_params,
                "result": log.response_result,
                "status": log.status,
                "error_msg": log.error_message,
                "execution_time": log.execution_time,
                "create_time": log.create_time.isoformat() if hasattr(log.create_time, 'isoformat') else log.create_time
            })

        return ResponseUtils.pagination(
            data=log_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取操作日志列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/statistics", response_model=AuthResponse, summary="获取操作日志统计", dependencies=[Depends(permission_dependency("log:view"))])
def get_operation_log_statistics(
    days: int = 7,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取操作日志统计接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        log_service = OperationLogService(db)
        statistics = log_service.get_statistics(tenant_id, days)

        return ResponseUtils.success(data=statistics, message="获取操作日志统计成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{log_id}", response_model=AuthResponse, summary="获取操作日志详情", dependencies=[Depends(permission_dependency("log:view"))])
def get_operation_log(
    log_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取操作日志详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        log_service = OperationLogService(db)
        log = log_service.get_log_by_id(log_id, tenant_id=tenant_id)

        description = log.description
        if not description and log.request_url:
            try:
                description = OperationLogUtils.generate_description(
                    log.request_url, 
                    log.request_method or "GET", 
                    log.module or "", 
                    log.operation or ""
                )
            except:
                pass

        log_info = {
            "id": log.id,
            "user_id": log.user_id,
            "username": log.username,
            "module": log.module,
            "operation": log.operation,
            "description": description,
            "method": log.request_method,
            "url": log.request_url,
            "ip": log.ip_address,
            "params": log.request_params,
            "result": log.response_result,
            "status": log.status,
            "error_msg": log.error_message,
            "execution_time": log.execution_time,
            "create_time": log.create_time.isoformat() if hasattr(log.create_time, 'isoformat') else log.create_time
        }

        return ResponseUtils.success(data=log_info, message="获取操作日志详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/cleanup", response_model=AuthResponse, summary="清理旧日志", dependencies=[Depends(permission_dependency("log:delete"))])
def cleanup_old_logs(
    days: int = 30,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """清理旧日志接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        log_service = OperationLogService(db)
        log_service.delete_old_logs(days, tenant_id=tenant_id)

        return ResponseUtils.success(message="清理旧日志成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
