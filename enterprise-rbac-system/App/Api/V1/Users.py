"""User Management API"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any
from fastapi.responses import JSONResponse
from App.Schemas.User import (
    UserCreate,
    UserUpdate,
    AssignRolesRequest,
    SetPrimaryRoleRequest
)
from App.Schemas.Auth import AuthResponse
from App.Services.UserService import UserService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Logger import logger
from App.Utils.Response import ResponseUtils
from App.Utils.ConfigManager import ConfigManager


router = APIRouter(
    prefix="/users",
    tags=["用户管理"]
)


@router.get("/me/permissions", response_model=AuthResponse, summary="获取当前用户权限列表")
def get_current_user_permissions(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取当前用户权限列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        
        user_service = UserService(db)

        from App.Repositories.UserRoleRepository import UserRoleRepository
        from App.Repositories.RolePermissionRepository import RolePermissionRepository
        from App.Repositories.PermissionRepository import PermissionRepository
        from App.Models.UserRole import UserRoleModel
        from App.Models.RolePermission import RolePermissionModel
        from App.Models.Permission import PermissionModel

        user_role_repo = UserRoleRepository(db)
        role_permission_repo = RolePermissionRepository(db)
        permission_repo = PermissionRepository(db)

        user_roles = user_role_repo.get_by_user_id(current_user.id, tenant_id=tenant_id)

        if not user_roles:
            return ResponseUtils.success(
                data=[],
                message="获取用户权限列表成功"
            )

        role_ids = [user_role.role_id for user_role in user_roles]
        
        role_permissions = db.query(RolePermissionModel).filter(
            RolePermissionModel.role_id.in_(role_ids),
            RolePermissionModel.tenant_id == tenant_id,
            RolePermissionModel.is_deleted == 0,
            RolePermissionModel.status == 1
        ).all()

        if not role_permissions:
            return ResponseUtils.success(
                data=[],
                message="获取用户权限列表成功"
            )

        permission_ids = [rp.permission_id for rp in role_permissions]
        
        permissions = db.query(PermissionModel).filter(
            PermissionModel.id.in_(permission_ids),
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0,
            PermissionModel.status == 1
        ).all()

        permission_codes = {perm.code for perm in permissions if perm.code}

        return ResponseUtils.success(
            data=list(permission_codes),
            message="获取用户权限列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/me/roles", response_model=AuthResponse, summary="获取当前用户角色列表")
def get_current_user_roles(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取当前用户角色列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_service = UserService(db)

        roles = user_service.get_user_roles(current_user.id, tenant_id=tenant_id)

        return ResponseUtils.success(
            data=roles,
            message="获取用户角色列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("", response_model=AuthResponse, summary="获取用户列表", dependencies=[Depends(permission_dependency("user:view"))])
def get_users(
    keyword: str = None,
    department_id: int = None,
    status: int = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> JSONResponse:
    """获取用户列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_service = UserService(db)

        total, users = user_service.paginate_users(
            tenant_id=tenant_id,
            keyword=keyword,
            department_id=department_id,
            status=status,
            page=page,
            page_size=page_size
        )

        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "email": user.email,
                "phone": user.phone,
                "avatar": user.avatar,
                "department_id": user.department_id,
                "status": user.status,
                "last_login_time": user.last_login_time if user.last_login_time else None,
                "last_login_ip": user.last_login_ip,
                "create_time": user.create_time.isoformat() if hasattr(user.create_time, 'isoformat') else user.create_time,
                "update_time": user.update_time.isoformat() if hasattr(user.update_time, 'isoformat') else user.update_time
            })

        return ResponseUtils.pagination(
            data=user_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取用户列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("", response_model=AuthResponse, summary="创建用户", dependencies=[Depends(permission_dependency("user:create"))])
def create_user(
    user_data: UserCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建用户接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_service = UserService(db)

        user_dict = user_data.model_dump()

        user = user_service.create_user(user_dict, tenant_id=tenant_id, created_by=current_user.id)

        user_info = {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "phone": user.phone,
            "avatar": user.avatar,
            "department_id": user.department_id,
            "status": user.status
        }

        return ResponseUtils.success(data=user_info, message="创建用户成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{user_id}", response_model=AuthResponse, summary="获取用户详情", dependencies=[Depends(permission_dependency("user:view"))])
def get_user(
    user_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取用户详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id, tenant_id=tenant_id)

        user_info = {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "phone": user.phone,
            "avatar": user.avatar,
            "department_id": user.department_id,
            "status": user.status,
            "last_login_time": user.last_login_time if user.last_login_time else None,
            "last_login_ip": user.last_login_ip,
            "create_time": user.create_time.isoformat() if hasattr(user.create_time, 'isoformat') else user.create_time,
            "update_time": user.update_time.isoformat() if hasattr(user.update_time, 'isoformat') else user.update_time
        }

        return ResponseUtils.success(data=user_info, message="获取用户详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{user_id}", response_model=AuthResponse, summary="更新用户信息", dependencies=[Depends(permission_dependency("user:update"))])
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新用户信息接口"""
    try:
        current_user, tenant_id = current_user_with_tenant

        user_service = UserService(db)
        user = user_service.update_user(user_id, user_data.model_dump(), tenant_id=tenant_id, updated_by=current_user.id)

        user_info = {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "phone": user.phone,
            "avatar": user.avatar,
            "department_id": user.department_id,
            "status": user.status
        }

        return ResponseUtils.success(data=user_info, message="更新用户信息成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/{user_id}", response_model=AuthResponse, summary="删除用户", dependencies=[Depends(permission_dependency("user:delete"))])
def delete_user(
    user_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除用户接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_service = UserService(db)
        user_service.delete_user(user_id, tenant_id=tenant_id)

        return ResponseUtils.success(message="删除用户成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{user_id}/status", response_model=AuthResponse, summary="更新用户状态", dependencies=[Depends(permission_dependency("user:update"))])
def update_user_status(
    user_id: int,
    status: int = None,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新用户状态接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        if status is None:
            return ResponseUtils.error(message="缺少状态参数", code=400, error_code=40000)

        user_service = UserService(db)
        user = user_service.update_user_status(user_id, status, tenant_id=tenant_id, updated_by=current_user.id)

        user_info = {
            "id": user.id,
            "username": user.username,
            "status": user.status
        }

        return ResponseUtils.success(data=user_info, message="更新用户状态成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("/{user_id}/avatar", response_model=AuthResponse, summary="上传用户头像", dependencies=[Depends(permission_dependency("user:update"))])
async def upload_avatar(
    user_id: int,
    file: UploadFile = File(...),
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """上传用户头像接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        file_extension = file.filename.split(".")[-1].lower()
        allowed_extensions = ConfigManager.get_list(db, "allowed_image_extensions", tenant_id)
        if file_extension not in allowed_extensions:
            return ResponseUtils.error(message=f"不支持的文件类型，仅支持{','.join(allowed_extensions)}", code=400, error_code=40000)

        import os
        import uuid
        file_name = f"{uuid.uuid4()}.{file_extension}"
        upload_dir = ConfigManager.get_str(db, "upload_dir", tenant_id, "./uploads")
        file_path = os.path.join(upload_dir, file_name)

        os.makedirs(upload_dir, exist_ok=True)

        file_size = 0
        chunk_size = 1024 * 1024
        max_file_size = ConfigManager.get_int(db, "max_file_size", tenant_id, 5242880)

        with open(file_path, "wb") as f:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                file_size += len(chunk)
                if file_size > max_file_size:
                    os.remove(file_path)
                    return ResponseUtils.error(message=f"文件大小超过限制，最大支持{max_file_size/1024/1024}MB", code=400, error_code=40000)
                f.write(chunk)

        user_service = UserService(db)
        user = user_service.update_user_avatar(user_id, file_path, tenant_id=tenant_id, updated_by=current_user.id)

        user_info = {
            "id": user.id,
            "username": user.username,
            "avatar": user.avatar
        }

        return ResponseUtils.success(data=user_info, message="上传头像成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{user_id}/roles", response_model=AuthResponse, summary="获取用户角色列表", dependencies=[Depends(permission_dependency("user:view"))])
def get_user_roles(
    user_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取用户角色列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_service = UserService(db)
        roles = user_service.get_user_roles(user_id, tenant_id=tenant_id)

        return ResponseUtils.success(
            data={
                "user_id": user_id,
                "roles": roles
            },
            message="获取用户角色列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{user_id}/roles", response_model=AuthResponse, summary="分配用户角色", dependencies=[Depends(permission_dependency("user:update"))])
def assign_roles(
    user_id: int,
    role_data: AssignRolesRequest,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """分配用户角色接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_service = UserService(db)
        user_service.assign_roles_to_user(user_id, role_data.role_ids, tenant_id=tenant_id, updated_by=current_user.id)

        return ResponseUtils.success(message="分配角色成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{user_id}/primary-role", response_model=AuthResponse, summary="设置用户主角色", dependencies=[Depends(permission_dependency("user:update"))])
def set_primary_role(
    user_id: int,
    role_data: SetPrimaryRoleRequest,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """设置用户主角色接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_service = UserService(db)
        user_service.set_primary_role(user_id, role_data.role_id, tenant_id=tenant_id, updated_by=current_user.id)

        return ResponseUtils.success(message="设置主角色成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{user_id}/reset-password", response_model=AuthResponse, summary="重置用户密码", dependencies=[Depends(permission_dependency("user:update"))])
def reset_password(
    user_id: int,
    password_data: Dict[str, Any],
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """重置用户密码接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        user_service = UserService(db)
        new_password = password_data.get("newPassword")
        if not new_password:
            return ResponseUtils.error(message="新密码不能为空", code=400, error_code=40000)
        user_service.reset_password(user_id, new_password, tenant_id=tenant_id, updated_by=current_user.id)

        return ResponseUtils.success(message="重置密码成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
