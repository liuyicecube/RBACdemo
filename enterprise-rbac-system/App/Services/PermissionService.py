"""Permission Service"""

from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from App.Models.Permission import PermissionModel
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Repositories.PermissionRepository import PermissionRepository
from App.Repositories.RolePermissionRepository import RolePermissionRepository
from App.Utils.Validators import Validators
from App.Utils.Logger import logger
from App.Utils.Cache import cache
from App.Config.CacheKeys import USER_PERMISSIONS, USER_MENU_TREE


class PermissionService:
    """权限服务类"""

    def __init__(self, db: Session):
        """初始化权限服务"""
        self.db = db
        self.permission_repository = PermissionRepository(db)
        self.role_permission_repository = RolePermissionRepository(db)

    def get_permission_by_id(self, permission_id: int, tenant_id: int):
        """根据ID获取权限"""
        permission = self.permission_repository.get_by_id(permission_id, tenant_id=tenant_id)
        if not permission:
            raise NotFoundException(detail="权限不存在")
        return permission

    def get_permission_by_code(self, code: str, tenant_id: int):
        """根据权限编码获取权限"""
        permission = self.permission_repository.get_by_code(code, tenant_id=tenant_id)
        if not permission:
            raise NotFoundException(detail="权限不存在")
        return permission

    def get_permissions(self, tenant_id: int, skip: int = 0, limit: int = 100):
        """获取权限列表"""
        return self.permission_repository.get_all(tenant_id=tenant_id, skip=skip, limit=limit)

    def get_active_permissions(self, tenant_id: int, skip: int = 0, limit: int = 100):
        """获取活跃权限列表"""
        return self.permission_repository.get_active_permissions(tenant_id=tenant_id, skip=skip, limit=limit)

    def get_permissions_by_type(self, permission_type: int, tenant_id: int, skip: int = 0, limit: int = 100):
        """根据权限类型获取权限列表"""
        if not Validators.is_type_valid(permission_type, [0, 1, 2, 3, 4]) :
            raise ValidationException(detail="无效的权限类型")

        return self.permission_repository.get_by_type(permission_type, tenant_id=tenant_id, skip=skip, limit=limit)

    def get_permissions_by_resource_type(self, resource_type: str, tenant_id: int, skip: int = 0, limit: int = 100):
        """根据资源类型获取权限列表"""
        return self.permission_repository.get_by_resource_type(resource_type, tenant_id=tenant_id, skip=skip, limit=limit)

    def get_permissions_by_parent_id(self, parent_id: int, tenant_id: int, skip: int = 0, limit: int = 100):
        """根据父权限ID获取子权限列表"""
        if parent_id != 0:
            parent_permission = self.permission_repository.get_by_id(parent_id, tenant_id=tenant_id)
            if not parent_permission:
                raise NotFoundException(detail="父权限不存在")

        return self.permission_repository.get_by_parent_id(parent_id, tenant_id=tenant_id, skip=skip, limit=limit)

    def get_by_action(self, action: str, tenant_id: int, skip: int = 0, limit: int = 100):
        """根据操作类型获取权限列表"""
        return self.permission_repository.get_by_action(action, tenant_id=tenant_id, skip=skip, limit=limit)

    def get_root_permissions(self, tenant_id: int, skip: int = 0, limit: int = 100):
        """获取根权限列表"""
        return self.permission_repository.get_root_permissions(tenant_id=tenant_id, skip=skip, limit=limit)

    def search_permissions(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100):
        """搜索权限"""
        return self.permission_repository.search(keyword, tenant_id=tenant_id, skip=skip, limit=limit)

    def paginate_permissions(
        self,
        tenant_id: int,
        keyword: str = None,
        permission_type: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ):
        """分页查询权限"""
        return self.permission_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            permission_type=permission_type,
            status=status,
            page=page,
            page_size=page_size
        )

    def create_permission(self, permission_data: Dict[str, Any], tenant_id: int, created_by: int):
        """创建权限"""
        permission_type = permission_data.get("type")
        if not Validators.is_type_valid(permission_type, [0, 1, 2, 3, 4]) :
            raise ValidationException(detail="无效的权限类型")

        action = permission_data.get("action")
        if action not in ['view', 'create', 'update', 'delete', 'export']:
            raise ValidationException(detail="无效的操作类型")

        method = permission_data.get("method")
        if method and method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']:
            raise ValidationException(detail="无效的HTTP方法")

        code = permission_data.get("code")
        existing_permission = self.permission_repository.get_by_code(code, tenant_id=tenant_id)
        if existing_permission:
            raise ValidationException(detail="权限编码已存在")

        parent_id = permission_data.get("parent_id")
        parent_level = 0
        if parent_id and parent_id != 0:
            parent_permission = self.permission_repository.get_by_id(parent_id, tenant_id=tenant_id)
            if not parent_permission:
                raise ValidationException(detail="父权限不存在")
            parent_level = parent_permission.level

        permission = PermissionModel(
            name=permission_data.get("name"),
            code=code,
            type=permission_type,
            resource_type=permission_data.get("resource_type"),
            resource_id=permission_data.get("resource_id"),
            action=action,
            path=permission_data.get("path"),
            method=method,
            parent_id=parent_id,
            level=parent_level + 1,
            status=permission_data.get("status", 1),
            description=permission_data.get("description"),
            tenant_id=tenant_id,
            created_by=created_by,
            updated_by=created_by
        )

        created_permission = self.permission_repository.create(permission)

        cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))

        logger.info(f"创建权限成功: {permission_data.get('name')}")

        return created_permission

    def update_permission(self, permission_id: int, permission_data: Dict[str, Any], tenant_id: int, updated_by: int):
        """更新权限"""
        permission = self.permission_repository.get_by_id(permission_id, tenant_id=tenant_id)
        if not permission:
            raise NotFoundException(detail="权限不存在")

        code = permission_data.get("code")
        if code and code != permission.code:
            existing_permission = self.permission_repository.get_by_code(code, tenant_id=tenant_id)
            if existing_permission:
                raise ValidationException(detail="权限编码已存在")
            permission.code = code

        if "type" in permission_data:
            permission_type = permission_data.get("type")
            if permission_type is not None and not Validators.is_type_valid(permission_type, [0, 1, 2, 3, 4]) :
                raise ValidationException(detail="无效的权限类型")
            elif permission_type is not None:
                permission.type = permission_type

        if "action" in permission_data:
            action = permission_data.get("action")
            if action is not None and action not in ['view', 'create', 'update', 'delete', 'export']:
                raise ValidationException(detail="无效的操作类型")
            elif action is not None:
                permission.action = action

        if "method" in permission_data:
            method = permission_data.get("method")
            if method and method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']:
                raise ValidationException(detail="无效的HTTP方法")
            permission.method = method

        if "parent_id" in permission_data:
            parent_id = permission_data.get("parent_id")
            if parent_id == 0 or parent_id is None:
                permission.parent_id = None
                permission.level = 1
            else:
                parent_permission = self.permission_repository.get_by_id(parent_id, tenant_id=tenant_id)
                if not parent_permission:
                    raise ValidationException(detail="父权限不存在")
                permission.parent_id = parent_id
                permission.level = parent_permission.level + 1

        if "name" in permission_data:
            permission.name = permission_data.get("name")

        if "resource_type" in permission_data:
            resource_type = permission_data.get("resource_type")
            if resource_type is not None:
                permission.resource_type = resource_type

        if "resource_id" in permission_data:
            permission.resource_id = permission_data.get("resource_id")

        if "path" in permission_data:
            path = permission_data.get("path")
            if path is not None:
                permission.path = path

        if "description" in permission_data:
            permission.description = permission_data.get("description")

        if "status" in permission_data:
            permission.status = permission_data.get("status")

        permission.updated_by = updated_by

        updated_permission = self.permission_repository.update(permission)

        cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))

        logger.info(f"更新权限成功: {permission.name}")

        return updated_permission

    def delete_permission(self, permission_id: int, tenant_id: int):
        """删除权限"""
        permission = self.permission_repository.get_by_id(permission_id, tenant_id=tenant_id)
        if not permission:
            raise NotFoundException(detail="权限不存在")

        children_permissions = self.permission_repository.get_by_parent_id(permission_id, tenant_id=tenant_id)
        if children_permissions:
            raise ValidationException(detail="该权限存在子权限，无法删除")

        role_count = self.role_permission_repository.count_by_permission_id(permission_id, tenant_id=tenant_id)
        if role_count > 0:
            raise ValidationException(detail=f"该权限已关联 {role_count} 个角色，无法删除")

        self.permission_repository.delete(permission)

        cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))

        logger.info(f"删除权限成功: {permission.name}")

        return True

    def update_permission_status(self, permission_id: int, status: int, tenant_id: int, updated_by: int):
        """更新权限状态"""
        if not Validators.is_status_valid(status):
            raise ValidationException(detail="无效的状态值")

        permission = self.permission_repository.get_by_id(permission_id, tenant_id=tenant_id)
        if not permission:
            raise NotFoundException(detail="权限不存在")

        permission.status = status
        permission.updated_by = updated_by

        updated_permission = self.permission_repository.update(permission)

        cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))

        logger.info(f"更新权限状态成功: {permission.name}, 状态: {status}")

        return updated_permission

    def get_permission_roles(self, permission_id: int, tenant_id: int):
        """获取权限关联的角色列表"""
        permission = self.permission_repository.get_by_id(permission_id, tenant_id=tenant_id)
        if not permission:
            raise NotFoundException(detail="权限不存在")

        role_permissions = self.role_permission_repository.get_by_permission_id(permission_id, tenant_id=tenant_id)

        roles = []
        for role_permission in role_permissions:
            role = role_permission.role
            roles.append({
                "id": role.id,
                "name": role.name,
                "code": role.code,
                "type": role.type,
                "status": role.status,
                "description": role.description
            })

        return roles

    def count_permission_roles(self, permission_id: int, tenant_id: int):
        """统计权限关联的角色数量"""
        permission = self.permission_repository.get_by_id(permission_id, tenant_id=tenant_id)
        if not permission:
            raise NotFoundException(detail="权限不存在")

        return self.role_permission_repository.count_by_permission_id(permission_id, tenant_id=tenant_id)

