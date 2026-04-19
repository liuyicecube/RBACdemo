"""Permission Management API"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from App.Schemas.Permission import (
    PermissionCreate,
    PermissionUpdate
)
from App.Schemas.Auth import AuthResponse
from App.Services.PermissionService import PermissionService
from App.Repositories.PermissionRepository import PermissionRepository
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/permissions",
    tags=["权限管理"]
)


@router.get(
    "",
    response_model=AuthResponse,
    summary="获取权限列表",
    dependencies=[Depends(permission_dependency("permission:view"))]
)
def get_permissions(
    keyword: str = None,
    type: int = None,
    resource_type: str = None,
    action: str = None,
    status: int = None,
    parent_id: int = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """获取权限列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_service = PermissionService(db)

        total, permissions = permission_service.paginate_permissions(
            tenant_id=tenant_id,
            keyword=keyword,
            permission_type=type,
            status=status,
            page=page,
            page_size=page_size
        )

        permission_list = []
        for perm in permissions:
            permission_list.append({
                "id": perm.id,
                "name": perm.name,
                "code": perm.code,
                "type": perm.type,
                "resource_type": perm.resource_type,
                "resource_id": perm.resource_id,
                "action": perm.action,
                "path": perm.path,
                "method": perm.method,
                "parent_id": perm.parent_id,
                "level": perm.level,
                "status": perm.status,
                "icon": perm.icon,
                "color": perm.color,
                "create_time": perm.create_time.isoformat() if hasattr(perm.create_time, 'isoformat') else perm.create_time,
                "update_time": perm.update_time.isoformat() if hasattr(perm.update_time, 'isoformat') else perm.update_time
            })

        return ResponseUtils.pagination(
            data=permission_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取权限列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/all",
    response_model=AuthResponse,
    summary="获取所有启用的权限（用于分配）",
    dependencies=[Depends(permission_dependency("permission:view"))]
)
def get_all_active_permissions(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """获取所有启用的权限接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_repo = PermissionRepository(db)
        permissions = permission_repo.get_active_permissions(
            tenant_id=tenant_id,
            skip=0,
            limit=10000
        )

        permission_list = []
        for perm in permissions:
            permission_list.append({
                "id": perm.id,
                "name": perm.name,
                "code": perm.code,
                "type": perm.type,
                "parent_id": perm.parent_id
            })

        return ResponseUtils.success(data=permission_list, message="获取所有启用的权限成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/{permission_id}",
    response_model=AuthResponse,
    summary="获取权限详情",
    dependencies=[Depends(permission_dependency("permission:view"))]
)
def get_permission(
    permission_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """获取权限详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_service = PermissionService(db)
        permission = permission_service.get_permission_by_id(permission_id, tenant_id=tenant_id)

        permission_info = {
            "id": permission.id,
            "name": permission.name,
            "code": permission.code,
            "type": permission.type,
            "resource_type": permission.resource_type,
            "resource_id": permission.resource_id,
            "action": permission.action,
            "path": permission.path,
            "method": permission.method,
            "parent_id": permission.parent_id,
            "level": permission.level,
            "status": permission.status,
            "icon": permission.icon,
            "color": permission.color,
            "create_time": permission.create_time.isoformat() if hasattr(permission.create_time, 'isoformat') else permission.create_time,
            "update_time": permission.update_time.isoformat() if hasattr(permission.update_time, 'isoformat') else permission.update_time
        }

        return ResponseUtils.success(data=permission_info, message="获取权限详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post(
    "",
    response_model=AuthResponse,
    summary="创建权限",
    dependencies=[Depends(permission_dependency("permission:create"))]
)
def create_permission(
    permission_data: PermissionCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """创建权限接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_service = PermissionService(db)
        permission = permission_service.create_permission(permission_data.model_dump(), tenant_id=tenant_id, created_by=current_user.id)

        permission_info = {
            "id": permission.id,
            "name": permission.name,
            "code": permission.code,
            "type": permission.type,
            "resource_type": permission.resource_type,
            "resource_id": permission.resource_id,
            "action": permission.action,
            "path": permission.path,
            "method": permission.method,
            "parent_id": permission.parent_id,
            "level": permission.level,
            "status": permission.status,
            "icon": permission.icon,
            "color": permission.color
        }

        return ResponseUtils.success(data=permission_info, message="创建权限成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put(
    "/{permission_id}",
    response_model=AuthResponse,
    summary="更新权限信息",
    dependencies=[Depends(permission_dependency("permission:update"))]
)
def update_permission(
    permission_id: int,
    permission_data: PermissionUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """更新权限信息接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_service = PermissionService(db)
        permission = permission_service.update_permission(permission_id, permission_data.model_dump(), tenant_id=tenant_id, updated_by=current_user.id)

        permission_info = {
            "id": permission.id,
            "name": permission.name,
            "code": permission.code,
            "type": permission.type,
            "resource_type": permission.resource_type,
            "resource_id": permission.resource_id,
            "action": permission.action,
            "path": permission.path,
            "method": permission.method,
            "parent_id": permission.parent_id,
            "level": permission.level,
            "status": permission.status,
            "icon": permission.icon,
            "color": permission.color
        }

        return ResponseUtils.success(data=permission_info, message="更新权限信息成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post(
    "/batch",
    response_model=AuthResponse,
    summary="批量创建权限",
    dependencies=[Depends(permission_dependency("permission:create"))]
)
def batch_create_permissions(
    permissions_data: List[PermissionCreate],
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """批量创建权限接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_service = PermissionService(db)
        created_permissions = []

        for perm_data in permissions_data:
            permission = permission_service.create_permission(perm_data.model_dump(), tenant_id=tenant_id, created_by=current_user.id)
            created_permissions.append(permission)

        permission_list = []
        for perm in created_permissions:
            permission_list.append({
                "id": perm.id,
                "name": perm.name,
                "code": perm.code,
                "type": perm.type,
                "status": perm.status
            })

        return ResponseUtils.success(
            data={
                "created_count": len(created_permissions),
                "permissions": permission_list
            },
            message="批量创建权限成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete(
    "/batch",
    response_model=AuthResponse,
    summary="批量删除权限",
    dependencies=[Depends(permission_dependency("permission:delete"))]
)
def batch_delete_permissions(
    permission_ids: List[int] = Query(..., description="权限ID列表"),
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """批量删除权限接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_service = PermissionService(db)
        deleted_count = 0

        for perm_id in permission_ids:
            try:
                permission_service.delete_permission(perm_id, tenant_id=tenant_id)
                deleted_count += 1
            except Exception:
                continue

        return ResponseUtils.success(
            data={
                "total_count": len(permission_ids),
                "deleted_count": deleted_count,
                "failed_count": len(permission_ids) - deleted_count
            },
            message="批量删除权限成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete(
    "/{permission_id}",
    response_model=AuthResponse,
    summary="删除权限",
    dependencies=[Depends(permission_dependency("permission:delete"))]
)
def delete_permission(
    permission_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """删除权限接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_service = PermissionService(db)
        permission_service.delete_permission(permission_id, tenant_id=tenant_id)

        return ResponseUtils.success(message="删除权限成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put(
    "/{permission_id}/status",
    response_model=AuthResponse,
    summary="更新权限状态",
    dependencies=[Depends(permission_dependency("permission:update"))]
)
def update_permission_status(
    permission_id: int,
    status: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """更新权限状态接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_service = PermissionService(db)
        permission = permission_service.update_permission_status(permission_id, status, tenant_id=tenant_id, updated_by=current_user.id)

        permission_info = {
            "id": permission.id,
            "name": permission.name,
            "status": permission.status
        }

        return ResponseUtils.success(data=permission_info, message="更新权限状态成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/{permission_id}/roles",
    response_model=AuthResponse,
    summary="获取权限关联的角色列表",
    dependencies=[Depends(permission_dependency("permission:view"))]
)
def get_permission_roles(
    permission_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """获取权限关联的角色列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_service = PermissionService(db)
        roles = permission_service.get_permission_roles(permission_id, tenant_id=tenant_id)

        return ResponseUtils.success(
            data={
                "permission_id": permission_id,
                "roles": roles
            },
            message="获取权限角色列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/{permission_id}/role-count",
    response_model=AuthResponse,
    summary="统计权限关联的角色数量",
    dependencies=[Depends(permission_dependency("permission:view"))]
)
def count_permission_roles(
    permission_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    """统计权限关联的角色数量接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        permission_service = PermissionService(db)
        role_count = permission_service.count_permission_roles(permission_id, tenant_id=tenant_id)

        return ResponseUtils.success(
            data={
                "permission_id": permission_id,
                "role_count": role_count
            },
            message="统计角色数量成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)

