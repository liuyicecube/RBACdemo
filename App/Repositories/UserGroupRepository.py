"""User Group Repository"""

from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from App.Models.UserGroup import UserGroupModel
from App.Repositories.Base import BaseRepository


class UserGroupRepository(BaseRepository[UserGroupModel]):
    """用户组仓储类"""

    def __init__(self, db: Session):
        """初始化用户组仓储"""
        super().__init__(db, UserGroupModel)

    def get_by_code(self, code: str, tenant_id: int) -> Optional[UserGroupModel]:
        """根据编码获取用户组"""
        return self.db.query(UserGroupModel).filter(
            UserGroupModel.code == code,
            UserGroupModel.tenant_id == tenant_id,
            UserGroupModel.is_deleted == 0
        ).first()

    def get_by_name(self, name: str, tenant_id: int) -> Optional[UserGroupModel]:
        """根据名称获取用户组"""
        return self.db.query(UserGroupModel).filter(
            UserGroupModel.name == name,
            UserGroupModel.tenant_id == tenant_id,
            UserGroupModel.is_deleted == 0
        ).first()

    def get_active_groups(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserGroupModel]:
        """获取所有启用的用户组"""
        return self.db.query(UserGroupModel).filter(
            UserGroupModel.tenant_id == tenant_id,
            UserGroupModel.is_deleted == 0,
            UserGroupModel.status == 1
        ).order_by(UserGroupModel.sort).offset(skip).limit(limit).all()

    def search(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserGroupModel]:
        """搜索用户组"""
        return self.db.query(UserGroupModel).filter(
            UserGroupModel.tenant_id == tenant_id,
            UserGroupModel.is_deleted == 0,
            or_(
                UserGroupModel.name.like(f"%{keyword}%"),
                UserGroupModel.code.like(f"%{keyword}%")
            )
        ).order_by(UserGroupModel.sort, UserGroupModel.create_time.desc()).offset(skip).limit(limit).all()

    def paginate(
        self,
        tenant_id: int,
        keyword: str = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[UserGroupModel]]:
        """分页查询用户组"""
        query = self.db.query(UserGroupModel).filter(
            UserGroupModel.tenant_id == tenant_id,
            UserGroupModel.is_deleted == 0
        )

        if keyword:
            query = query.filter(
                or_(
                    UserGroupModel.name.like(f"%{keyword}%"),
                    UserGroupModel.code.like(f"%{keyword}%")
                )
            )

        if status is not None:
            query = query.filter(UserGroupModel.status == status)

        total = query.count()
        items = query.order_by(UserGroupModel.sort, UserGroupModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return total, items
