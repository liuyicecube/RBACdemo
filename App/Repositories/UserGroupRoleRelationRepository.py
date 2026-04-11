"""User Group Role Relation Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from App.Models.UserGroupRoleRelation import UserGroupRoleRelationModel
from App.Repositories.Base import BaseRepository


class UserGroupRoleRelationRepository(BaseRepository[UserGroupRoleRelationModel]):
    """用户组-角色关联仓储类"""
    
    def __init__(self, db: Session):
        """初始化用户组-角色关联仓储"""
        super().__init__(db, UserGroupRoleRelationModel)
    
    def get_by_group_id(self, user_group_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserGroupRoleRelationModel]:
        """根据用户组ID获取关联角色"""
        return self.db.query(UserGroupRoleRelationModel).filter(
            UserGroupRoleRelationModel.user_group_id == user_group_id,
            UserGroupRoleRelationModel.tenant_id == tenant_id,
            UserGroupRoleRelationModel.is_deleted == 0,
            UserGroupRoleRelationModel.status == 1
        ).offset(skip).limit(limit).all()
    
    def get_by_role_id(self, role_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserGroupRoleRelationModel]:
        """根据角色ID获取关联用户组"""
        return self.db.query(UserGroupRoleRelationModel).filter(
            UserGroupRoleRelationModel.role_id == role_id,
            UserGroupRoleRelationModel.tenant_id == tenant_id,
            UserGroupRoleRelationModel.is_deleted == 0,
            UserGroupRoleRelationModel.status == 1
        ).offset(skip).limit(limit).all()
    
    def delete_by_group_id(self, user_group_id: int, tenant_id: int) -> None:
        """根据用户组ID删除所有角色关联"""
        self.db.query(UserGroupRoleRelationModel).filter(
            UserGroupRoleRelationModel.user_group_id == user_group_id,
            UserGroupRoleRelationModel.tenant_id == tenant_id
        ).delete()
        self.db.commit()
    
    def delete_by_role_id(self, role_id: int, tenant_id: int) -> None:
        """根据角色ID删除所有用户组关联"""
        self.db.query(UserGroupRoleRelationModel).filter(
            UserGroupRoleRelationModel.role_id == role_id,
            UserGroupRoleRelationModel.tenant_id == tenant_id
        ).delete()
        self.db.commit()
