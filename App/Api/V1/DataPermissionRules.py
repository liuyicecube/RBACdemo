"""Data Permission Rule Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from App.Schemas.DataPermissionRule import (
    DataPermissionRuleCreate,
    DataPermissionRuleUpdate
)
from App.Schemas.Auth import AuthResponse
from App.Services.DataPermissionRuleService import DataPermissionRuleService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Logger import logger
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/data-permission-rules",
    tags=["数据权限规则管理"]
)


@router.get("", response_model=AuthResponse, summary="获取数据权限规则列表", dependencies=[Depends(permission_dependency("data_permission:view"))])
def get_data_permission_rules(
    keyword: str = None,
    permission_id: int = None,
    rule_type: int = None,
    status: int = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取数据权限规则列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        rule_service = DataPermissionRuleService(db)

        total, rules = rule_service.paginate_rules(
            tenant_id=tenant_id,
            keyword=keyword,
            permission_id=permission_id,
            rule_type=rule_type,
            status=status,
            page=page,
            page_size=page_size
        )

        rule_list = []
        for rule in rules:
            rule_list.append({
                "id": rule.id,
                "name": rule.name,
                "code": rule.code,
                "permission_id": rule.permission_id,
                "resource_table": rule.resource_table,
                "rule_type": rule.rule_type,
                "rule_expression": rule.rule_expression,
                "description": rule.description,
                "status": rule.status,
                "create_time": rule.create_time.isoformat() if hasattr(rule.create_time, 'isoformat') else rule.create_time,
                "update_time": rule.update_time.isoformat() if hasattr(rule.update_time, 'isoformat') else rule.update_time
            })

        return ResponseUtils.pagination(
            data=rule_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取数据权限规则列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_data_permission_rules: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/all", response_model=AuthResponse, summary="获取所有启用的数据权限规则", dependencies=[Depends(permission_dependency("data_permission:view"))])
def get_all_active_rules(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取所有启用的数据权限规则接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        rule_service = DataPermissionRuleService(db)
        rules = rule_service.get_active_rules(tenant_id=tenant_id)

        rule_list = []
        for rule in rules:
            rule_list.append({
                "id": rule.id,
                "name": rule.name,
                "code": rule.code,
                "permission_id": rule.permission_id,
                "resource_table": rule.resource_table,
                "rule_type": rule.rule_type
            })

        return ResponseUtils.success(data=rule_list, message="获取所有启用的数据权限规则成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{rule_id}", response_model=AuthResponse, summary="获取数据权限规则详情", dependencies=[Depends(permission_dependency("data_permission:view"))])
def get_data_permission_rule(
    rule_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取数据权限规则详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        rule_service = DataPermissionRuleService(db)
        rule = rule_service.get_rule_by_id(rule_id, tenant_id=tenant_id)

        rule_info = {
            "id": rule.id,
            "name": rule.name,
            "code": rule.code,
            "permission_id": rule.permission_id,
            "resource_table": rule.resource_table,
            "rule_type": rule.rule_type,
            "rule_expression": rule.rule_expression,
            "description": rule.description,
            "status": rule.status,
            "create_time": rule.create_time.isoformat() if hasattr(rule.create_time, 'isoformat') else rule.create_time,
            "update_time": rule.update_time.isoformat() if hasattr(rule.update_time, 'isoformat') else rule.update_time
        }

        return ResponseUtils.success(data=rule_info, message="获取数据权限规则详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_data_permission_rule: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("", response_model=AuthResponse, summary="创建数据权限规则", dependencies=[Depends(permission_dependency("data_permission:create"))])
def create_data_permission_rule(
    rule_data: DataPermissionRuleCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建数据权限规则接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        rule_service = DataPermissionRuleService(db)

        rule = rule_service.create_rule(rule_data.model_dump(), tenant_id=tenant_id, created_by=current_user.id)

        rule_info = {
            "id": rule.id,
            "name": rule.name,
            "code": rule.code,
            "permission_id": rule.permission_id,
            "resource_table": rule.resource_table,
            "rule_type": rule.rule_type
        }

        return ResponseUtils.success(data=rule_info, message="创建数据权限规则成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in create_data_permission_rule: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{rule_id}", response_model=AuthResponse, summary="更新数据权限规则", dependencies=[Depends(permission_dependency("data_permission:update"))])
def update_data_permission_rule(
    rule_id: int,
    rule_data: DataPermissionRuleUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新数据权限规则接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        rule_service = DataPermissionRuleService(db)
        rule = rule_service.update_rule(rule_id, rule_data.model_dump(exclude_unset=True), tenant_id=tenant_id, updated_by=current_user.id)

        rule_info = {
            "id": rule.id,
            "name": rule.name,
            "code": rule.code,
            "permission_id": rule.permission_id,
            "resource_table": rule.resource_table,
            "rule_type": rule.rule_type
        }

        return ResponseUtils.success(data=rule_info, message="更新数据权限规则成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in update_data_permission_rule: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/{rule_id}", response_model=AuthResponse, summary="删除数据权限规则", dependencies=[Depends(permission_dependency("data_permission:delete"))])
def delete_data_permission_rule(
    rule_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除数据权限规则接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        rule_service = DataPermissionRuleService(db)
        rule_service.delete_rule(rule_id, tenant_id=tenant_id)

        return ResponseUtils.success(message="删除数据权限规则成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{rule_id}/status", response_model=AuthResponse, summary="更新数据权限规则状态", dependencies=[Depends(permission_dependency("data_permission:update"))])
def update_data_permission_rule_status(
    rule_id: int,
    status: int = None,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新数据权限规则状态接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        if status is None:
            return ResponseUtils.error(message="缺少状态参数", code=400, error_code=40000)

        rule_service = DataPermissionRuleService(db)
        rule = rule_service.update_rule_status(rule_id, status, tenant_id=tenant_id, updated_by=current_user.id)

        rule_info = {
            "id": rule.id,
            "name": rule.name,
            "status": rule.status
        }

        return ResponseUtils.success(data=rule_info, message="更新数据权限规则状态成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("/{rule_id}/test", response_model=AuthResponse, summary="测试数据权限规则", dependencies=[Depends(permission_dependency("data_permission:view"))])
def test_data_permission_rule(
    rule_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """测试数据权限规则接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        rule_service = DataPermissionRuleService(db)
        test_result = rule_service.test_rule(rule_id, tenant_id=tenant_id)

        return ResponseUtils.success(data=test_result, message="测试数据权限规则成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
