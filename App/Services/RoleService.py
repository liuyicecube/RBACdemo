"""Role Service"""

from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from App.Models.Role import RoleModel
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Repositories.RoleRepository import RoleRepository
from App.Repositories.RolePermissionRepository import RolePermissionRepository
from App.Utils.Validators import Validators
from App.Utils.Logger import logger
from App.Utils.Cache import cache
from App.Config.CacheKeys import USER_PERMISSIONS, USER_MENU_TREE


class RoleService:
    """角色服务类"""
    
    def __init__(self, db: Session):
        """初始化角色服务"""
        self.db = db
        self.role_repository = RoleRepository(db)
        self.role_permission_repository = RolePermissionRepository(db)
        from App.Repositories.UserRoleRepository import UserRoleRepository
        from App.Repositories.PermissionRepository import PermissionRepository
        self.user_role_repository = UserRoleRepository(db)
        self.permission_repository = PermissionRepository(db)
    
    def get_role_by_id(self, role_id: int, tenant_id: int) -> RoleModel:
        """根据ID获取角色"""
        role = self.role_repository.get_by_id(role_id, tenant_id=tenant_id)
        if not role:
            raise NotFoundException(detail="角色不存在")
        return role
    
    def get_role_by_code(self, code: str, tenant_id: int) -> RoleModel:
        """根据角色编码获取角色"""
        role = self.role_repository.get_by_code(code, tenant_id=tenant_id)
        if not role:
            raise NotFoundException(detail="角色不存在")
        return role
    
    def get_roles(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """获取角色列表"""
        return self.role_repository.get_all(tenant_id=tenant_id, skip=skip, limit=limit)
    
    def get_active_roles(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """获取活跃角色列表"""
        return self.role_repository.get_active_roles(tenant_id=tenant_id, skip=skip, limit=limit)
    
    def get_roles_by_type(self, role_type: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """根据角色类型获取角色列表"""
        if not Validators.is_type_valid(role_type, [0, 1, 2, 3]) :
            raise ValidationException(detail="无效的角色类型")
        
        return self.role_repository.get_by_type(role_type, tenant_id=tenant_id, skip=skip, limit=limit)
    
    def get_roles_by_parent_id(self, parent_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """根据父角色ID获取子角色列表"""
        if parent_id != 0:
            parent_role = self.role_repository.get_by_id(parent_id, tenant_id=tenant_id)
            if not parent_role:
                raise NotFoundException(detail="父角色不存在")
        
        return self.role_repository.get_by_parent_id(parent_id, tenant_id=tenant_id, skip=skip, limit=limit)
    
    def get_root_roles(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """获取根角色列表"""
        return self.role_repository.get_root_roles(tenant_id=tenant_id, skip=skip, limit=limit)
    
    def search_roles(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """搜索角色"""
        return self.role_repository.search(keyword, tenant_id=tenant_id, skip=skip, limit=limit)
    
    def paginate_roles(
        self,
        tenant_id: int,
        keyword: str = None,
        role_type: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[RoleModel]]:
        """分页查询角色"""
        return self.role_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            role_type=role_type,
            status=status,
            page=page,
            page_size=page_size
        )
    
    def create_role(self, role_data: Dict[str, Any], tenant_id: int, created_by: int) -> RoleModel:
        """创建角色"""
        role_type = role_data.get("type", 3)
        if not Validators.is_type_valid(role_type, [0, 1, 2, 3]) :
            raise ValidationException(detail="无效的角色类型")
        
        code = role_data.get("code")
        existing_role = self.role_repository.get_by_code(code, tenant_id=tenant_id)
        if existing_role:
            raise ValidationException(detail="角色编码已存在")
        
        name = role_data.get("name")
        existing_role = self.role_repository.get_by_name(name, tenant_id=tenant_id)
        if existing_role:
            raise ValidationException(detail="角色名称已存在")
        
        parent_id = role_data.get("parent_id")
        parent_level = 0
        if parent_id and parent_id != 0:
            parent_role = self.role_repository.get_by_id(parent_id, tenant_id=tenant_id)
            if not parent_role:
                raise ValidationException(detail="父角色不存在")
            parent_level = parent_role.level
        
        role = RoleModel(
            name=name,
            code=code,
            parent_id=parent_id,
            level=parent_level + 1,
            type=role_type,
            data_scope=role_data.get("data_scope", 0),
            sort=role_data.get("sort", 0),
            description=role_data.get("description"),
            status=role_data.get("status", 1),
            tenant_id=tenant_id,
            created_by=created_by,
            updated_by=created_by
        )
        
        created_role = self.role_repository.create(role)
        
        logger.info(f"创建角色成功: {name}")
        
        return created_role
    
    def update_role(self, role_id: int, role_data: Dict[str, Any], tenant_id: int, updated_by: int) -> RoleModel:
        """更新角色"""
        role = self.role_repository.get_by_id(role_id, tenant_id=tenant_id)
        if not role:
            raise NotFoundException(detail="角色不存在")
        
        code = role_data.get("code")
        if code and code != role.code:
            existing_role = self.role_repository.get_by_code(code, tenant_id=tenant_id)
            if existing_role:
                raise ValidationException(detail="角色编码已存在")
            role.code = code
        
        name = role_data.get("name")
        if name and name != role.name:
            existing_role = self.role_repository.get_by_name(name, tenant_id=tenant_id)
            if existing_role:
                raise ValidationException(detail="角色名称已存在")
            role.name = name
        
        parent_id = role_data.get("parent_id")
        if parent_id is not None:
            if parent_id == 0 or parent_id is None:
                role.parent_id = None
                role.level = 1
            else:
                parent_role = self.role_repository.get_by_id(parent_id, tenant_id=tenant_id)
                if not parent_role:
                    raise ValidationException(detail="父角色不存在")
                if parent_id == role_id:
                    raise ValidationException(detail="父角色不能是自身")
                children_ids = self.role_repository.get_role_children_ids(role_id, tenant_id=tenant_id)
                if parent_id in children_ids:
                    raise ValidationException(detail="存在循环依赖")
                role.parent_id = parent_id
                role.level = parent_role.level + 1
        
        if "description" in role_data:
            role.description = role_data.get("description")
        
        if "type" in role_data:
            role_type = role_data.get("type")
            if role_type is not None and not Validators.is_type_valid(role_type, [0, 1, 2, 3]) :
                raise ValidationException(detail="无效的角色类型")
            elif role_type is not None:
                role.type = role_type
        
        if "data_scope" in role_data:
            data_scope = role_data.get("data_scope")
            if data_scope is not None:
                role.data_scope = data_scope
        
        if "sort" in role_data:
            sort = role_data.get("sort")
            if sort is not None:
                role.sort = sort
        
        if "status" in role_data:
            role.status = role_data.get("status")
        
        role.updated_by = updated_by
        
        updated_role = self.role_repository.update(role)
        
        logger.info(f"更新角色成功: {role.name}")
        
        return updated_role
    
    def delete_role(self, role_id: int, tenant_id: int) -> bool:
        """删除角色"""
        role = self.role_repository.get_by_id(role_id, tenant_id=tenant_id)
        if not role:
            raise NotFoundException(detail="角色不存在")
        
        children_roles = self.role_repository.get_by_parent_id(role_id, tenant_id=tenant_id)
        if children_roles:
            raise ValidationException(detail="该角色存在子角色，无法删除")
        
        user_count = self.user_role_repository.count_by_role_id(role_id, tenant_id=tenant_id)
        if user_count > 0:
            raise ValidationException(detail=f"该角色已关联 {user_count} 个用户，无法删除")
        
        self.role_permission_repository.delete_by_role_id(role_id, tenant_id=tenant_id)
        
        self.role_repository.delete(role)
        
        logger.info(f"删除角色成功: {role.name}")
        
        return True
    
    def update_role_status(self, role_id: int, status: int, tenant_id: int, updated_by: int) -> RoleModel:
        """更新角色状态"""
        if not Validators.is_status_valid(status):
            raise ValidationException(detail="无效的状态值")
        
        role = self.role_repository.get_by_id(role_id, tenant_id=tenant_id)
        if not role:
            raise NotFoundException(detail="角色不存在")
        
        role.status = status
        role.updated_by = updated_by
        
        updated_role = self.role_repository.update(role)
        
        logger.info(f"更新角色状态成功: {role.name}, 状态: {status}")
        
        return updated_role
    
    def get_role_permissions(self, role_id: int, tenant_id: int) -> List[Dict[str, Any]]:
        """获取角色权限列表"""
        role = self.role_repository.get_by_id(role_id, tenant_id=tenant_id)
        if not role:
            raise NotFoundException(detail="角色不存在")
        
        role_permissions = self.role_permission_repository.get_by_role_id(role_id, tenant_id=tenant_id)
        
        permissions = []
        for role_permission in role_permissions:
            permission = role_permission.permission
            permissions.append({
                "id": permission.id,
                "name": permission.name,
                "code": permission.code,
                "type": permission.type,
                "resource_type": permission.resource_type,
                "action": permission.action,
                "path": permission.path,
                "method": permission.method
            })
        
        return permissions
    
    def assign_permissions_to_role(self, role_id: int, permission_ids: List[int], tenant_id: int, updated_by: int) -> bool:
        """分配权限给角色"""
        role = self.role_repository.get_by_id(role_id, tenant_id=tenant_id)
        if not role:
            raise NotFoundException(detail="角色不存在")
        
        for permission_id in permission_ids:
            permission = self.permission_repository.get_by_id(permission_id, tenant_id=tenant_id)
            if not permission:
                raise ValidationException(detail=f"权限ID {permission_id} 不存在")
        
        self.role_permission_repository.bulk_create(role_id, permission_ids, tenant_id=tenant_id, operator_id=updated_by)
        
        cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"分配权限给角色成功: {role.name}")
        
        return True
    
    def remove_permission_from_role(self, role_id: int, permission_id: int, tenant_id: int) -> bool:
        """从角色中移除权限"""
        role = self.role_repository.get_by_id(role_id, tenant_id=tenant_id)
        if not role:
            raise NotFoundException(detail="角色不存在")
        
        permission = self.permission_repository.get_by_id(permission_id, tenant_id=tenant_id)
        if not permission:
            raise NotFoundException(detail="权限不存在")
        
        role_permission = self.role_permission_repository.get_by_role_and_permission(role_id, permission_id, tenant_id=tenant_id)
        if not role_permission:
            raise NotFoundException(detail="角色未关联该权限")
        
        self.role_permission_repository.delete(role_permission)
        
        cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"从角色中移除权限成功: {role.name}, 权限: {permission.name}")
        
        return True
    
    def get_role_children(self, role_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """获取角色的所有子角色"""
        role = self.role_repository.get_by_id(role_id, tenant_id=tenant_id)
        if not role:
            raise NotFoundException(detail="角色不存在")
        
        return self.role_repository.get_by_parent_id(role_id, tenant_id=tenant_id, skip=skip, limit=limit)
    
    def count_role_users(self, role_id: int, tenant_id: int) -> int:
        """统计角色关联的用户数量"""
        role = self.role_repository.get_by_id(role_id, tenant_id=tenant_id)
        if not role:
            raise NotFoundException(detail="角色不存在")
        
        return self.user_role_repository.count_by_role_id(role_id, tenant_id=tenant_id)
