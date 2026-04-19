"""Role Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from App.Schemas.Role import (
    RoleCreate,
    RoleUpdate,
    AssignPermissionsRequest
)
from App.Schemas.Auth import AuthResponse
from App.Services.RoleService import RoleService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency

from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/roles",
    tags=["角色管理"]
)


@router.get("", response_model=AuthResponse, summary="获取角色列表", dependencies=[Depends(permission_dependency("role:view"))])
def get_roles(
    keyword: str = None,
    status: int = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取角色列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        role_service = RoleService(db)

        total, roles = role_service.paginate_roles(
            tenant_id=tenant_id,
            keyword=keyword,
            status=status,
            page=page,
            page_size=page_size
        )

        role_list = []
        for role in roles:
            role_list.append({
                "id": role.id,
                "name": role.name,
                "code": role.code,
                "description": role.description,
                "sort_order": role.sort,
                "sort": role.sort,
                "status": role.status,
                "type": role.type,
                "data_scope": role.data_scope,
                "dataScope": role.data_scope,
                "parent_id": role.parent_id,
                "parentId": role.parent_id,
                "icon": role.icon,
                "color": role.color,
                "create_time": role.create_time.isoformat() if hasattr(role.create_time, 'isoformat') else role.create_time,
                "update_time": role.update_time.isoformat() if hasattr(role.update_time, 'isoformat') else role.update_time
            })

        return ResponseUtils.pagination(
            data=role_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取角色列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/all", response_model=AuthResponse, summary="获取所有角色（用于下拉选择）", dependencies=[Depends(permission_dependency("role:view"))])
def get_all_roles(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取所有角色接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        role_service = RoleService(db)
        roles = role_service.get_roles(tenant_id=tenant_id, skip=0, limit=1000)
        
        role_list = []
        for role in roles:
            # 确保 status 是整数类型
            status_val = int(role.status) if role.status is not None else 1
            
            role_data = {
                "id": role.id,
                "name": role.name,
                "code": role.code,
                "status": status_val,  # 确保返回整数
                "description": role.description,
                "icon": role.icon,
                "color": role.color,
                "type": role.type
            }
            
            role_list.append(role_data)
        return ResponseUtils.success(data=role_list, message="获取所有启用的角色成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{role_id}", response_model=AuthResponse, summary="获取角色详情", dependencies=[Depends(permission_dependency("role:view"))])
def get_role(
    role_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取角色详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        role_service = RoleService(db)
        role = role_service.get_role_by_id(role_id, tenant_id=tenant_id)

        role_info = {
            "id": role.id,
            "name": role.name,
            "code": role.code,
            "description": role.description,
            "sort_order": role.sort,
            "sort": role.sort,
            "status": role.status,
            "type": role.type,
            "data_scope": role.data_scope,
            "dataScope": role.data_scope,
            "parent_id": role.parent_id,
            "parentId": role.parent_id,
            "icon": role.icon,
            "color": role.color,
            "create_time": role.create_time.isoformat() if hasattr(role.create_time, 'isoformat') else role.create_time,
            "update_time": role.update_time.isoformat() if hasattr(role.update_time, 'isoformat') else role.update_time
        }

        return ResponseUtils.success(data=role_info, message="获取角色详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("", response_model=AuthResponse, summary="创建角色", dependencies=[Depends(permission_dependency("role:create"))])
def create_role(
    role_data: RoleCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建角色接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        role_service = RoleService(db)

        role = role_service.create_role(role_data.model_dump(), tenant_id=tenant_id, created_by=current_user.id)

        role_info = {
            "id": role.id,
            "name": role.name,
            "code": role.code,
            "description": role.description,
            "sort_order": role.sort,
            "sort": role.sort,
            "status": role.status,
            "type": role.type,
            "data_scope": role.data_scope,
            "dataScope": role.data_scope,
            "parent_id": role.parent_id,
            "parentId": role.parent_id,
            "icon": role.icon,
            "color": role.color
        }

        return ResponseUtils.success(data=role_info, message="创建角色成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{role_id}", response_model=AuthResponse, summary="更新角色信息", dependencies=[Depends(permission_dependency("role:update"))])
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新角色信息接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        role_service = RoleService(db)
        role = role_service.update_role(role_id, role_data.model_dump(), tenant_id=tenant_id, updated_by=current_user.id)

        role_info = {
            "id": role.id,
            "name": role.name,
            "code": role.code,
            "description": role.description,
            "sort_order": role.sort,
            "sort": role.sort,
            "status": role.status,
            "type": role.type,
            "data_scope": role.data_scope,
            "dataScope": role.data_scope,
            "parent_id": role.parent_id,
            "parentId": role.parent_id,
            "icon": role.icon,
            "color": role.color
        }

        return ResponseUtils.success(data=role_info, message="更新角色信息成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/{role_id}", response_model=AuthResponse, summary="删除角色", dependencies=[Depends(permission_dependency("role:delete"))])
def delete_role(
    role_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除角色接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        role_service = RoleService(db)
        role_service.delete_role(role_id, tenant_id=tenant_id)

        return ResponseUtils.success(message="删除角色成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{role_id}/status", response_model=AuthResponse, summary="更新角色状态", dependencies=[Depends(permission_dependency("role:update"))])
def update_role_status(
    role_id: int,
    status: int = None,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新角色状态接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        if status is None:
            return ResponseUtils.error(message="缺少状态参数", code=400, error_code=40000)

        role_service = RoleService(db)
        role = role_service.update_role_status(role_id, status, tenant_id=tenant_id, updated_by=current_user.id)

        role_info = {
            "id": role.id,
            "name": role.name,
            "status": role.status
        }

        return ResponseUtils.success(data=role_info, message="更新角色状态成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{role_id}/permissions", response_model=AuthResponse, summary="获取角色权限列表", dependencies=[Depends(permission_dependency("role:view"))])
def get_role_permissions(
    role_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取角色权限列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        role_service = RoleService(db)
        permissions = role_service.get_role_permissions(role_id, tenant_id=tenant_id)

        return ResponseUtils.success(
            data={
                "role_id": role_id,
                "permissions": permissions
            },
            message="获取角色权限列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{role_id}/permissions", response_model=AuthResponse, summary="分配角色权限", dependencies=[Depends(permission_dependency("role:update"))])
def assign_permissions(
    role_id: int,
    permission_data: AssignPermissionsRequest,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """分配角色权限接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        role_service = RoleService(db)
        role_service.assign_permissions_to_role(role_id, permission_data.permission_ids, tenant_id=tenant_id, updated_by=current_user.id)

        return ResponseUtils.success(message="分配权限成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{role_id}/users", response_model=AuthResponse, summary="获取角色用户列表", dependencies=[Depends(permission_dependency("role:view"))])
def get_role_users(
    role_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取角色用户列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        role_service = RoleService(db)
        users = role_service.get_role_users(role_id, tenant_id=tenant_id)

        return ResponseUtils.success(
            data={
                "role_id": role_id,
                "users": users
            },
            message="获取角色用户列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
