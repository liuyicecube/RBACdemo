"""User Group Service"""

from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from App.Models.UserGroup import UserGroupModel
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Repositories.UserGroupRepository import UserGroupRepository
from App.Repositories.UserGroupRelationRepository import UserGroupRelationRepository
from App.Repositories.UserGroupRoleRelationRepository import UserGroupRoleRelationRepository
from App.Utils.Validators import Validators
from App.Utils.Logger import logger
from App.Utils.Cache import cache
from App.Config.CacheKeys import USER_PERMISSIONS, USER_MENU_TREE


class UserGroupService:
    """用户组服务类"""
    
    def __init__(self, db: Session):
        """初始化用户组服务"""
        self.db = db
        self.user_group_repository = UserGroupRepository(db)
        self.user_group_relation_repository = UserGroupRelationRepository(db)
        self.user_group_role_relation_repository = UserGroupRoleRelationRepository(db)
        from App.Repositories.UserRepository import UserRepository
        from App.Repositories.RoleRepository import RoleRepository
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)
    
    def get_user_group_by_id(self, user_group_id: int, tenant_id: int) -> UserGroupModel:
        """根据ID获取用户组"""
        user_group = self.user_group_repository.get_by_id(user_group_id, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        return user_group
    
    def get_user_group_by_code(self, code: str, tenant_id: int) -> UserGroupModel:
        """根据编码获取用户组"""
        user_group = self.user_group_repository.get_by_code(code, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        return user_group
    
    def get_user_groups(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserGroupModel]:
        """获取用户组列表"""
        return self.user_group_repository.get_all(tenant_id=tenant_id, skip=skip, limit=limit)
    
    def get_active_user_groups(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserGroupModel]:
        """获取活跃用户组列表"""
        return self.user_group_repository.get_active_groups(tenant_id=tenant_id, skip=skip, limit=limit)
    
    def search_user_groups(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserGroupModel]:
        """搜索用户组"""
        return self.user_group_repository.search(keyword, tenant_id=tenant_id, skip=skip, limit=limit)
    
    def paginate_user_groups(
        self,
        tenant_id: int,
        keyword: str = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[UserGroupModel]]:
        """分页查询用户组"""
        return self.user_group_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            status=status,
            page=page,
            page_size=page_size
        )
    
    def create_user_group(self, user_group_data: Dict[str, Any], tenant_id: int, created_by: int) -> UserGroupModel:
        """创建用户组"""
        code = user_group_data.get("code")
        existing_user_group = self.user_group_repository.get_by_code(code, tenant_id=tenant_id)
        if existing_user_group:
            raise ValidationException(detail="用户组编码已存在")
        
        name = user_group_data.get("name")
        existing_user_group = self.user_group_repository.get_by_name(name, tenant_id=tenant_id)
        if existing_user_group:
            raise ValidationException(detail="用户组名称已存在")
        
        user_group = UserGroupModel(
            name=name,
            code=code,
            description=user_group_data.get("description"),
            sort=user_group_data.get("sort", 0),
            status=user_group_data.get("status", 1),
            tenant_id=tenant_id,
            created_by=created_by,
            updated_by=created_by
        )
        
        created_user_group = self.user_group_repository.create(user_group)
        
        logger.info(f"创建用户组成功: {name}")
        
        return created_user_group
    
    def update_user_group(self, user_group_id: int, user_group_data: Dict[str, Any], tenant_id: int, updated_by: int) -> UserGroupModel:
        """更新用户组"""
        user_group = self.user_group_repository.get_by_id(user_group_id, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        
        code = user_group_data.get("code")
        if code and code != user_group.code:
            existing_user_group = self.user_group_repository.get_by_code(code, tenant_id=tenant_id)
            if existing_user_group:
                raise ValidationException(detail="用户组编码已存在")
            user_group.code = code
        
        name = user_group_data.get("name")
        if name and name != user_group.name:
            existing_user_group = self.user_group_repository.get_by_name(name, tenant_id=tenant_id)
            if existing_user_group:
                raise ValidationException(detail="用户组名称已存在")
            user_group.name = name
        
        if "description" in user_group_data:
            user_group.description = user_group_data.get("description")
        
        if "sort" in user_group_data:
            user_group.sort = user_group_data.get("sort")
        
        if "status" in user_group_data:
            user_group.status = user_group_data.get("status")
        
        user_group.updated_by = updated_by
        
        updated_user_group = self.user_group_repository.update(user_group)
        
        logger.info(f"更新用户组成功: {user_group.name}")
        
        return updated_user_group
    
    def delete_user_group(self, user_group_id: int, tenant_id: int) -> bool:
        """删除用户组"""
        user_group = self.user_group_repository.get_by_id(user_group_id, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        
        self.user_group_relation_repository.delete_by_group_id(user_group_id, tenant_id=tenant_id)
        self.user_group_role_relation_repository.delete_by_group_id(user_group_id, tenant_id=tenant_id)
        
        self.user_group_repository.delete(user_group)
        
        logger.info(f"删除用户组成功: {user_group.name}")
        
        return True
    
    def update_user_group_status(self, user_group_id: int, status: int, tenant_id: int, updated_by: int) -> UserGroupModel:
        """更新用户组状态"""
        if not Validators.is_status_valid(status):
            raise ValidationException(detail="无效的状态值")
        
        user_group = self.user_group_repository.get_by_id(user_group_id, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        
        user_group.status = status
        user_group.updated_by = updated_by
        
        updated_user_group = self.user_group_repository.update(user_group)
        
        logger.info(f"更新用户组状态成功: {user_group.name}, 状态: {status}")
        
        return updated_user_group
    
    def get_user_group_users(self, user_group_id: int, tenant_id: int) -> List[Dict[str, Any]]:
        """获取用户组成员"""
        user_group = self.user_group_repository.get_by_id(user_group_id, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        
        relations = self.user_group_relation_repository.get_by_group_id(user_group_id, tenant_id=tenant_id)
        
        users = []
        for relation in relations:
            user = relation.user
            users.append({
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "email": user.email,
                "status": user.status
            })
        
        return users
    
    def assign_users_to_user_group(self, user_group_id: int, user_ids: List[int], tenant_id: int, operator_id: int) -> bool:
        """分配用户到用户组"""
        user_group = self.user_group_repository.get_by_id(user_group_id, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        
        for user_id in user_ids:
            user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
            if not user:
                raise ValidationException(detail=f"用户ID {user_id} 不存在")
        
        from App.Models.UserGroupRelation import UserGroupRelationModel
        for user_id in user_ids:
            existing = self.db.query(UserGroupRelationModel).filter(
                UserGroupRelationModel.user_group_id == user_group_id,
                UserGroupRelationModel.user_id == user_id,
                UserGroupRelationModel.tenant_id == tenant_id,
                UserGroupRelationModel.is_deleted == 0
            ).first()
            
            if not existing:
                relation = UserGroupRelationModel(
                    user_group_id=user_group_id,
                    user_id=user_id,
                    tenant_id=tenant_id,
                    created_by=operator_id,
                    updated_by=operator_id
                )
                self.db.add(relation)
        
        self.db.commit()
        
        cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"分配用户到用户组成功: {user_group.name}")
        
        return True
    
    def remove_users_from_user_group(self, user_group_id: int, user_ids: List[int], tenant_id: int) -> bool:
        """从用户组移除用户"""
        user_group = self.user_group_repository.get_by_id(user_group_id, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        
        from App.Models.UserGroupRelation import UserGroupRelationModel
        for user_id in user_ids:
            relation = self.db.query(UserGroupRelationModel).filter(
                UserGroupRelationModel.user_group_id == user_group_id,
                UserGroupRelationModel.user_id == user_id,
                UserGroupRelationModel.tenant_id == tenant_id,
                UserGroupRelationModel.is_deleted == 0
            ).first()
            
            if relation:
                relation.is_deleted = 1
                self.db.add(relation)
        
        self.db.commit()
        
        cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"从用户组移除用户成功: {user_group.name}")
        
        return True
    
    def get_user_group_roles(self, user_group_id: int, tenant_id: int) -> List[Dict[str, Any]]:
        """获取用户组角色"""
        user_group = self.user_group_repository.get_by_id(user_group_id, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        
        relations = self.user_group_role_relation_repository.get_by_group_id(user_group_id, tenant_id=tenant_id)
        
        roles = []
        for relation in relations:
            role = relation.role
            roles.append({
                "id": role.id,
                "name": role.name,
                "code": role.code,
                "status": role.status
            })
        
        return roles
    
    def assign_roles_to_user_group(self, user_group_id: int, role_ids: List[int], tenant_id: int, operator_id: int) -> bool:
        """分配角色到用户组"""
        user_group = self.user_group_repository.get_by_id(user_group_id, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        
        for role_id in role_ids:
            role = self.role_repository.get_by_id(role_id, tenant_id=tenant_id)
            if not role:
                raise ValidationException(detail=f"角色ID {role_id} 不存在")
        
        from App.Models.UserGroupRoleRelation import UserGroupRoleRelationModel
        for role_id in role_ids:
            existing = self.db.query(UserGroupRoleRelationModel).filter(
                UserGroupRoleRelationModel.user_group_id == user_group_id,
                UserGroupRoleRelationModel.role_id == role_id,
                UserGroupRoleRelationModel.tenant_id == tenant_id,
                UserGroupRoleRelationModel.is_deleted == 0
            ).first()
            
            if not existing:
                relation = UserGroupRoleRelationModel(
                    user_group_id=user_group_id,
                    role_id=role_id,
                    tenant_id=tenant_id,
                    created_by=operator_id,
                    updated_by=operator_id
                )
                self.db.add(relation)
        
        self.db.commit()
        
        cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"分配角色到用户组成功: {user_group.name}")
        
        return True
    
    def remove_roles_from_user_group(self, user_group_id: int, role_ids: List[int], tenant_id: int) -> bool:
        """从用户组移除角色"""
        user_group = self.user_group_repository.get_by_id(user_group_id, tenant_id=tenant_id)
        if not user_group:
            raise NotFoundException(detail="用户组不存在")
        
        from App.Models.UserGroupRoleRelation import UserGroupRoleRelationModel
        for role_id in role_ids:
            relation = self.db.query(UserGroupRoleRelationModel).filter(
                UserGroupRoleRelationModel.user_group_id == user_group_id,
                UserGroupRoleRelationModel.role_id == role_id,
                UserGroupRoleRelationModel.tenant_id == tenant_id,
                UserGroupRoleRelationModel.is_deleted == 0
            ).first()
            
            if relation:
                relation.is_deleted = 1
                self.db.add(relation)
        
        self.db.commit()
        
        cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"从用户组移除角色成功: {user_group.name}")
        
        return True
