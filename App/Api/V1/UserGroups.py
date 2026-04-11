"""User Group Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from App.Schemas.UserGroup import (
    UserGroupCreate,
    UserGroupUpdate,
    AssignUsersRequest,
    AssignRolesRequest
)
from App.Schemas.Auth import AuthResponse
from App.Services.UserGroupService import UserGroupService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Logger import logger
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/user-groups",
    tags=["用户组管理"]
)


@router.get("", response_model=AuthResponse, summary="获取用户组列表", dependencies=[Depends(permission_dependency("user_group:view"))])
def get_user_groups(
    keyword: str = None,
    status: int = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取用户组列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        
        total, user_groups = user_group_service.paginate_user_groups(
            tenant_id=tenant_id,
            keyword=keyword,
            status=status,
            page=page,
            page_size=page_size
        )
        
        user_group_list = []
        for user_group in user_groups:
            user_group_list.append({
                "id": user_group.id,
                "name": user_group.name,
                "code": user_group.code,
                "description": user_group.description,
                "sort": user_group.sort,
                "status": user_group.status,
                "create_time": user_group.create_time.isoformat() if hasattr(user_group.create_time, 'isoformat') else user_group.create_time,
                "update_time": user_group.update_time.isoformat() if hasattr(user_group.update_time, 'isoformat') else user_group.update_time
            })
        
        return ResponseUtils.pagination(
            data=user_group_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取用户组列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_user_groups: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/all", response_model=AuthResponse, summary="获取所有启用的用户组（用于下拉选择）", dependencies=[Depends(permission_dependency("user_group:view"))])
def get_all_active_user_groups(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取所有启用的用户组接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        user_groups = user_group_service.get_active_user_groups(tenant_id=tenant_id)
        
        user_group_list = []
        for user_group in user_groups:
            user_group_list.append({
                "id": user_group.id,
                "name": user_group.name,
                "code": user_group.code
            })
        
        return ResponseUtils.success(data=user_group_list, message="获取所有启用的用户组成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{user_group_id}", response_model=AuthResponse, summary="获取用户组详情", dependencies=[Depends(permission_dependency("user_group:view"))])
def get_user_group(
    user_group_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取用户组详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        user_group = user_group_service.get_user_group_by_id(user_group_id, tenant_id=tenant_id)
        
        user_group_info = {
            "id": user_group.id,
            "name": user_group.name,
            "code": user_group.code,
            "description": user_group.description,
            "sort": user_group.sort,
            "status": user_group.status,
            "create_time": user_group.create_time.isoformat() if hasattr(user_group.create_time, 'isoformat') else user_group.create_time,
            "update_time": user_group.update_time.isoformat() if hasattr(user_group.update_time, 'isoformat') else user_group.update_time
        }
        
        return ResponseUtils.success(data=user_group_info, message="获取用户组详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_user_group: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("", response_model=AuthResponse, summary="创建用户组", dependencies=[Depends(permission_dependency("user_group:create"))])
def create_user_group(
    user_group_data: UserGroupCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建用户组接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        
        user_group = user_group_service.create_user_group(user_group_data.model_dump(), tenant_id=tenant_id, created_by=current_user.id)
        
        user_group_info = {
            "id": user_group.id,
            "name": user_group.name,
            "code": user_group.code,
            "description": user_group.description,
            "sort": user_group.sort,
            "status": user_group.status
        }
        
        return ResponseUtils.success(data=user_group_info, message="创建用户组成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in create_user_group: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{user_group_id}", response_model=AuthResponse, summary="更新用户组信息", dependencies=[Depends(permission_dependency("user_group:update"))])
def update_user_group(
    user_group_id: int,
    user_group_data: UserGroupUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新用户组信息接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        user_group = user_group_service.update_user_group(user_group_id, user_group_data.model_dump(), tenant_id=tenant_id, updated_by=current_user.id)
        
        user_group_info = {
            "id": user_group.id,
            "name": user_group.name,
            "code": user_group.code,
            "description": user_group.description,
            "sort": user_group.sort,
            "status": user_group.status
        }
        
        return ResponseUtils.success(data=user_group_info, message="更新用户组信息成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in update_user_group: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/{user_group_id}", response_model=AuthResponse, summary="删除用户组", dependencies=[Depends(permission_dependency("user_group:delete"))])
def delete_user_group(
    user_group_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除用户组接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        user_group_service.delete_user_group(user_group_id, tenant_id=tenant_id)
        
        return ResponseUtils.success(message="删除用户组成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{user_group_id}/status", response_model=AuthResponse, summary="更新用户组状态", dependencies=[Depends(permission_dependency("user_group:update"))])
def update_user_group_status(
    user_group_id: int,
    status: int = None,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新用户组状态接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        if status is None:
            return ResponseUtils.error(message="缺少状态参数", code=400, error_code=40000)
        
        user_group_service = UserGroupService(db)
        user_group = user_group_service.update_user_group_status(user_group_id, status, tenant_id=tenant_id, updated_by=current_user.id)
        
        user_group_info = {
            "id": user_group.id,
            "name": user_group.name,
            "status": user_group.status
        }
        
        return ResponseUtils.success(data=user_group_info, message="更新用户组状态成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{user_group_id}/users", response_model=AuthResponse, summary="获取用户组成员", dependencies=[Depends(permission_dependency("user_group:view"))])
def get_user_group_users(
    user_group_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取用户组成员接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        users = user_group_service.get_user_group_users(user_group_id, tenant_id=tenant_id)
        
        return ResponseUtils.success(
            data={
                "user_group_id": user_group_id,
                "users": users
            },
            message="获取用户组成员成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{user_group_id}/users", response_model=AuthResponse, summary="分配用户到用户组", dependencies=[Depends(permission_dependency("user_group:update"))])
def assign_users(
    user_group_id: int,
    user_data: AssignUsersRequest,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """分配用户到用户组接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        user_group_service.assign_users_to_user_group(user_group_id, user_data.user_ids, tenant_id=tenant_id, operator_id=current_user.id)
        
        return ResponseUtils.success(message="分配用户成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in assign_users: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/{user_group_id}/users", response_model=AuthResponse, summary="从用户组移除用户", dependencies=[Depends(permission_dependency("user_group:update"))])
def remove_users(
    user_group_id: int,
    user_data: AssignUsersRequest,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """从用户组移除用户接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        user_group_service.remove_users_from_user_group(user_group_id, user_data.user_ids, tenant_id=tenant_id)
        
        return ResponseUtils.success(message="移除用户成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{user_group_id}/roles", response_model=AuthResponse, summary="获取用户组角色", dependencies=[Depends(permission_dependency("user_group:view"))])
def get_user_group_roles(
    user_group_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取用户组角色接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        roles = user_group_service.get_user_group_roles(user_group_id, tenant_id=tenant_id)
        
        return ResponseUtils.success(
            data={
                "user_group_id": user_group_id,
                "roles": roles
            },
            message="获取用户组角色成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{user_group_id}/roles", response_model=AuthResponse, summary="分配角色到用户组", dependencies=[Depends(permission_dependency("user_group:update"))])
def assign_roles(
    user_group_id: int,
    role_data: AssignRolesRequest,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """分配角色到用户组接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        user_group_service.assign_roles_to_user_group(user_group_id, role_data.role_ids, tenant_id=tenant_id, operator_id=current_user.id)
        
        return ResponseUtils.success(message="分配角色成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in assign_roles: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/{user_group_id}/roles", response_model=AuthResponse, summary="从用户组移除角色", dependencies=[Depends(permission_dependency("user_group:update"))])
def remove_roles(
    user_group_id: int,
    role_data: AssignRolesRequest,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """从用户组移除角色接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_group_service = UserGroupService(db)
        user_group_service.remove_roles_from_user_group(user_group_id, role_data.role_ids, tenant_id=tenant_id)
        
        return ResponseUtils.success(message="移除角色成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
