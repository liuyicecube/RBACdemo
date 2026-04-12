"""User Group Relation Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from App.Models.UserGroupRelation import UserGroupRelationModel
from App.Repositories.Base import BaseRepository


class UserGroupRelationRepository(BaseRepository[UserGroupRelationModel]):
    """用户组-用户关联仓储类"""

    def __init__(self, db: Session):
        """初始化用户组-用户关联仓储"""
        super().__init__(db, UserGroupRelationModel)

    def get_by_user_id(self, user_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserGroupRelationModel]:
        """根据用户ID获取所属用户组"""
        return self.db.query(UserGroupRelationModel).filter(
            UserGroupRelationModel.user_id == user_id,
            UserGroupRelationModel.tenant_id == tenant_id,
            UserGroupRelationModel.is_deleted == 0,
            UserGroupRelationModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_by_group_id(self, user_group_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserGroupRelationModel]:
        """根据用户组ID获取组内用户"""
        return self.db.query(UserGroupRelationModel).filter(
            UserGroupRelationModel.user_group_id == user_group_id,
            UserGroupRelationModel.tenant_id == tenant_id,
            UserGroupRelationModel.is_deleted == 0,
            UserGroupRelationModel.status == 1
        ).offset(skip).limit(limit).all()

    def delete_by_user_id(self, user_id: int, tenant_id: int) -> None:
        """根据用户ID删除所有组关联"""
        self.db.query(UserGroupRelationModel).filter(
            UserGroupRelationModel.user_id == user_id,
            UserGroupRelationModel.tenant_id == tenant_id
        ).delete()
        self.db.commit()

    def delete_by_group_id(self, user_group_id: int, tenant_id: int) -> None:
        """根据用户组ID删除所有用户关联"""
        self.db.query(UserGroupRelationModel).filter(
            UserGroupRelationModel.user_group_id == user_group_id,
            UserGroupRelationModel.tenant_id == tenant_id
        ).delete()
        self.db.commit()
