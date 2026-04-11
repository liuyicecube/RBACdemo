"""Audit Log Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
from App.Schemas.Auth import AuthResponse
from App.Services.AuditLogService import AuditLogService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/audit-logs",
    tags=["审计日志管理"]
)


@router.get("", response_model=AuthResponse, summary="获取审计日志列表", dependencies=[Depends(permission_dependency("audit:view"))])
def get_audit_logs(
    keyword: str = None,
    table_name: str = None,
    record_id: int = None,
    operation_type: str = None,
    user_id: int = None,
    start_time: str = None,
    end_time: str = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取审计日志列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        log_service = AuditLogService(db)
        
        start_datetime = None
        end_datetime = None
        if start_time:
            start_datetime = datetime.fromisoformat(start_time)
        if end_time:
            end_datetime = datetime.fromisoformat(end_time)
        
        total, logs = log_service.paginate_logs(
            tenant_id=tenant_id,
            keyword=keyword,
            table_name=table_name,
            record_id=record_id,
            operation_type=operation_type,
            user_id=user_id,
            start_time=start_datetime,
            end_time=end_datetime,
            page=page,
            page_size=page_size
        )
        
        log_list = []
        for log in logs:
            log_list.append({
                "id": log.id,
                "user_id": log.user_id,
                "username": log.username,
                "table_name": log.table_name,
                "record_id": log.record_id,
                "operation_type": log.operation_type,
                "old_value": log.old_value,
                "new_value": log.new_value,
                "change_fields": log.change_fields,
                "create_time": log.create_time.isoformat() if hasattr(log.create_time, 'isoformat') else log.create_time
            })
        
        return ResponseUtils.pagination(
            data=log_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取审计日志列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_audit_logs: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/statistics", response_model=AuthResponse, summary="获取审计日志统计", dependencies=[Depends(permission_dependency("audit:view"))])
def get_audit_log_statistics(
    days: int = 7,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取审计日志统计接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        log_service = AuditLogService(db)
        statistics = log_service.get_statistics(tenant_id, days)
        
        return ResponseUtils.success(data=statistics, message="获取审计日志统计成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_audit_log_statistics: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{log_id}", response_model=AuthResponse, summary="获取审计日志详情", dependencies=[Depends(permission_dependency("audit:view"))])
def get_audit_log(
    log_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取审计日志详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        log_service = AuditLogService(db)
        log = log_service.get_log_by_id(log_id, tenant_id=tenant_id)
        
        log_info = {
            "id": log.id,
            "user_id": log.user_id,
            "username": log.username,
            "table_name": log.table_name,
            "record_id": log.record_id,
            "operation_type": log.operation_type,
            "old_value": log.old_value,
            "new_value": log.new_value,
            "change_fields": log.change_fields,
            "create_time": log.create_time.isoformat() if hasattr(log.create_time, 'isoformat') else log.create_time
        }
        
        return ResponseUtils.success(data=log_info, message="获取审计日志详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_audit_log: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/record/{table_name}/{record_id}", response_model=AuthResponse, summary="获取记录变更历史", dependencies=[Depends(permission_dependency("audit:view"))])
def get_record_change_history(
    table_name: str,
    record_id: int,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取记录变更历史接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        log_service = AuditLogService(db)
        total, logs = log_service.get_logs_by_record(table_name, record_id, tenant_id, page, page_size)
        
        log_list = []
        for log in logs:
            log_list.append({
                "id": log.id,
                "user_id": log.user_id,
                "username": log.username,
                "operation_type": log.operation_type,
                "old_value": log.old_value,
                "new_value": log.new_value,
                "change_fields": log.change_fields,
                "create_time": log.create_time.isoformat() if hasattr(log.create_time, 'isoformat') else log.create_time
            })
        
        return ResponseUtils.pagination(
            data=log_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取记录变更历史成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_record_change_history: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/cleanup", response_model=AuthResponse, summary="清理旧日志", dependencies=[Depends(permission_dependency("audit:delete"))])
def cleanup_old_logs(
    days: int = 90,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """清理旧日志接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        log_service = AuditLogService(db)
        log_service.delete_old_logs(days, tenant_id=tenant_id)
        
        return ResponseUtils.success(message="清理旧日志成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in cleanup_old_logs: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
