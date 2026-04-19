"""Permission Dependencies"""

from fastapi import Depends, Request
from sqlalchemy.orm import Session
from typing import List
from App.Models.Role import RoleModel
from App.Models.Permission import PermissionModel
from App.Models.RolePermission import RolePermissionModel
from App.Core.Exceptions import PermissionException
from App.Dependencies.Auth import get_current_user, get_current_user_and_tenant_id
from App.Dependencies.Database import get_db
from App.Utils.Cache import cache
from App.Config.CacheKeys import USER_PERMISSIONS, CACHE_EXPIRE_1_HOUR


def permission_dependency(required_permission: str):
    """权限验证依赖工厂函数"""

    def check_permission(
        request: Request,
        db: Session = Depends(get_db)
    ) -> bool:
        """检查用户是否具有所需权限"""
        # 获取当前用户和租户ID
        current_user, tenant_id = get_current_user_and_tenant_id(request, db)

        # 使用统一的缓存键常量
        cache_key = USER_PERMISSIONS.format(user_id=current_user.id)

        # 从数据库查询用户的所有角色
        from App.Models.UserRole import UserRoleModel
        user_roles = db.query(RoleModel).join(
            UserRoleModel, UserRoleModel.role_id == RoleModel.id
        ).filter(
            UserRoleModel.user_id == current_user.id,
            UserRoleModel.tenant_id == tenant_id,
            UserRoleModel.is_deleted == 0,
            RoleModel.tenant_id == tenant_id,
            RoleModel.is_deleted == 0,
            RoleModel.status == 1
        ).all()

        if not user_roles:
            raise PermissionException(detail="用户未分配角色")

        # 获取角色ID列表
        role_ids = [role.id for role in user_roles]

        # 获取所有相关权限
        permissions = db.query(PermissionModel).join(
            RolePermissionModel
        ).filter(
            RolePermissionModel.role_id.in_(role_ids),
            RolePermissionModel.tenant_id == tenant_id,
            RolePermissionModel.is_deleted == 0,
            RolePermissionModel.status == 1,
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0,
            PermissionModel.status == 1
        ).all()

        # 提取权限代码列表
        permission_codes = [perm.code for perm in permissions]

        # 缓存用户权限，使用统一的过期时间常量
        cache.set_json(cache_key, permission_codes, expire=CACHE_EXPIRE_1_HOUR)

        # 检查是否具有所需权限
        if required_permission not in permission_codes:
            raise PermissionException(detail=f"缺少权限：{required_permission}")

        return True

    return check_permission


def get_user_permissions(
    request: Request,
    db: Session = Depends(get_db)
) -> List[PermissionModel]:
    """获取当前用户的所有权限"""
    # 获取当前用户和租户ID
    current_user, tenant_id = get_current_user_and_tenant_id(request, db)

    # 使用统一的缓存键常量
    cache_key = USER_PERMISSIONS.format(user_id=current_user.id)

    # 从数据库查询用户的所有角色
    from App.Models.UserRole import UserRoleModel
    user_roles = db.query(RoleModel).join(
        UserRoleModel, UserRoleModel.role_id == RoleModel.id
    ).filter(
        UserRoleModel.user_id == current_user.id,
        UserRoleModel.tenant_id == tenant_id,
        UserRoleModel.is_deleted == 0,
        RoleModel.tenant_id == tenant_id,
        RoleModel.is_deleted == 0,
        RoleModel.status == 1
    ).all()

    if not user_roles:
        return []

    # 获取角色ID列表
    role_ids = [role.id for role in user_roles]

    # 获取所有相关权限
    permissions = db.query(PermissionModel).join(
        RolePermissionModel
    ).filter(
        RolePermissionModel.role_id.in_(role_ids),
        RolePermissionModel.tenant_id == tenant_id,
        RolePermissionModel.is_deleted == 0,
        RolePermissionModel.status == 1,
        PermissionModel.tenant_id == tenant_id,
        PermissionModel.is_deleted == 0,
        PermissionModel.status == 1
    ).all()

    # 提取权限代码列表并缓存
    permission_codes = [perm.code for perm in permissions]
    cache.set_json(cache_key, permission_codes, expire=CACHE_EXPIRE_1_HOUR)

    return permissions
