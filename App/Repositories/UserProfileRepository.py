"""User Profile Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from App.Models.UserProfile import UserProfileModel
from App.Repositories.Base import BaseRepository


class UserProfileRepository(BaseRepository[UserProfileModel]):
    """用户资料仓储类"""

    def __init__(self, db: Session):
        """初始化用户资料仓储"""
        super().__init__(db, UserProfileModel)

    def get_by_user_id(self, user_id: int, tenant_id: int) -> Optional[UserProfileModel]:
        """根据用户ID获取用户资料"""
        return self.db.query(UserProfileModel).filter(
            UserProfileModel.user_id == user_id,
            UserProfileModel.tenant_id == tenant_id,
            UserProfileModel.is_deleted == 0
        ).first()

    def get_all(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserProfileModel]:
        """获取所有用户资料"""
        return self.db.query(UserProfileModel).filter(
            UserProfileModel.tenant_id == tenant_id,
            UserProfileModel.is_deleted == 0
        ).offset(skip).limit(limit).all()

    def get_by_gender(self, gender: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserProfileModel]:
        """根据性别获取用户资料"""
        return self.db.query(UserProfileModel).filter(
            UserProfileModel.gender == gender,
            UserProfileModel.tenant_id == tenant_id,
            UserProfileModel.is_deleted == 0
        ).offset(skip).limit(limit).all()

    def get_by_position(self, position: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserProfileModel]:
        """根据职位获取用户资料"""
        return self.db.query(UserProfileModel).filter(
            UserProfileModel.position == position,
            UserProfileModel.tenant_id == tenant_id,
            UserProfileModel.is_deleted == 0
        ).offset(skip).limit(limit).all()

    def delete_by_user_id(self, user_id: int, tenant_id: int) -> bool:
        """根据用户ID删除用户资料"""
        profile = self.get_by_user_id(user_id, tenant_id=tenant_id)
        if profile:
            self.delete(profile)
            return True
        return False
