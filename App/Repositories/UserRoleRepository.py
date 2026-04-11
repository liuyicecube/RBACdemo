"""User Role Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from App.Models.UserRole import UserRoleModel
from App.Repositories.Base import BaseRepository


class UserRoleRepository(BaseRepository[UserRoleModel]):
    """用户角色关联仓储类"""
    
    def __init__(self, db: Session):
        """初始化用户角色关联仓储"""
        super().__init__(db, UserRoleModel)
    
    def get_by_user_id(self, user_id: int, tenant_id: int) -> List[UserRoleModel]:
        """根据用户ID获取角色关联"""
        return self.db.query(UserRoleModel).filter(
            UserRoleModel.user_id == user_id,
            UserRoleModel.tenant_id == tenant_id,
            UserRoleModel.is_deleted == 0,
            UserRoleModel.status == 1
        ).all()
    
    def get_by_role_id(self, role_id: int, tenant_id: int) -> List[UserRoleModel]:
        """根据角色ID获取用户关联"""
        return self.db.query(UserRoleModel).filter(
            UserRoleModel.role_id == role_id,
            UserRoleModel.tenant_id == tenant_id,
            UserRoleModel.is_deleted == 0,
            UserRoleModel.status == 1
        ).all()
    
    def get_by_user_and_role(self, user_id: int, role_id: int, tenant_id: int) -> Optional[UserRoleModel]:
        """根据用户ID和角色ID获取关联"""
        return self.db.query(UserRoleModel).filter(
            UserRoleModel.user_id == user_id,
            UserRoleModel.role_id == role_id,
            UserRoleModel.tenant_id == tenant_id,
            UserRoleModel.is_deleted == 0
        ).first()
    
    def delete_by_user_id(self, user_id: int, tenant_id: int) -> None:
        """根据用户ID删除所有角色关联"""
        self.db.query(UserRoleModel).filter(
            UserRoleModel.user_id == user_id,
            UserRoleModel.tenant_id == tenant_id
        ).delete()
        self.db.commit()
    
    def delete_by_role_id(self, role_id: int, tenant_id: int) -> None:
        """根据角色ID删除所有用户关联"""
        self.db.query(UserRoleModel).filter(
            UserRoleModel.role_id == role_id,
            UserRoleModel.tenant_id == tenant_id
        ).delete()
        self.db.commit()
    
    def get_primary_role(self, user_id: int, tenant_id: int) -> Optional[UserRoleModel]:
        """获取用户的主角色"""
        return self.db.query(UserRoleModel).filter(
            UserRoleModel.user_id == user_id,
            UserRoleModel.tenant_id == tenant_id,
            UserRoleModel.is_deleted == 0,
            UserRoleModel.is_primary == True,
            UserRoleModel.status == 1
        ).first()
    
    def count_by_role_id(self, role_id: int, tenant_id: int) -> int:
        """统计角色关联的用户数量"""
        return self.db.query(UserRoleModel).filter(
            UserRoleModel.role_id == role_id,
            UserRoleModel.tenant_id == tenant_id,
            UserRoleModel.is_deleted == 0,
            UserRoleModel.status == 1
        ).count()
    
    def count_by_user_id(self, user_id: int, tenant_id: int) -> int:
        """统计用户关联的角色数量"""
        return self.db.query(UserRoleModel).filter(
            UserRoleModel.user_id == user_id,
            UserRoleModel.tenant_id == tenant_id,
            UserRoleModel.is_deleted == 0,
            UserRoleModel.status == 1
        ).count()
    
    def batch_assign_roles(self, user_id: int, role_ids: List[int], tenant_id: int, operator_id: int = None) -> None:
        """批量为用户分配角色"""
        self.delete_by_user_id(user_id, tenant_id)
        for role_id in role_ids:
            user_role = UserRoleModel(
                user_id=user_id,
                role_id=role_id,
                tenant_id=tenant_id,
                created_by=operator_id
            )
            self.db.add(user_role)
        self.db.commit()