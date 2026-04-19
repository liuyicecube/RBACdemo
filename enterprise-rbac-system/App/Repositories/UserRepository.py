"""User Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from App.Models.User import UserModel
from App.Repositories.Base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    """用户仓储类"""

    def __init__(self, db: Session):
        """初始化用户仓储"""
        super().__init__(db, UserModel)

    def get_by_username(
        self,
        username: str,
        tenant_id: int = None,
        include_deleted: bool = False
    ) -> Optional[UserModel]:
        """根据用户名获取用户"""
        query = self.db.query(UserModel).filter(UserModel.username == username)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.first()

    def get_by_email(
        self,
        email: str,
        tenant_id: int = None,
        include_deleted: bool = False
    ) -> Optional[UserModel]:
        """根据邮箱获取用户"""
        query = self.db.query(UserModel).filter(UserModel.email == email)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.first()

    def get_by_phone(
        self,
        phone: str,
        tenant_id: int = None,
        include_deleted: bool = False
    ) -> Optional[UserModel]:
        """根据手机号获取用户"""
        query = self.db.query(UserModel).filter(UserModel.phone == phone)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.first()

    def get_by_department(
        self,
        department_id: int,
        tenant_id: int = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False
    ) -> List[UserModel]:
        """根据部门ID获取用户"""
        query = self.db.query(UserModel).filter(
            UserModel.department_id == department_id,
            UserModel.status == 1
        )
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.offset(skip).limit(limit).all()

    def search(
        self,
        keyword: str,
        tenant_id: int = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False
    ) -> List[UserModel]:
        """搜索用户"""
        query = self.db.query(UserModel).filter(
            or_(
                UserModel.username.like(f"%{keyword}%"),
                UserModel.nickname.like(f"%{keyword}%"),
                UserModel.email.like(f"%{keyword}%"),
                UserModel.phone.like(f"%{keyword}%")
            ),
            UserModel.status == 1
        )
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.offset(skip).limit(limit).all()

    def get_active_users(
        self,
        tenant_id: int = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False
    ) -> List[UserModel]:
        """获取活跃用户"""
        query = self.db.query(UserModel).filter(UserModel.status == 1)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.offset(skip).limit(limit).all()

    def get_inactive_users(
        self,
        tenant_id: int = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False
    ) -> List[UserModel]:
        """获取非活跃用户"""
        query = self.db.query(UserModel).filter(UserModel.status == 0)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.offset(skip).limit(limit).all()

    def paginate(
        self,
        tenant_id: int = None,
        keyword: str = None,
        department_id: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20,
        include_deleted: bool = False
    ) -> tuple[int, List[UserModel]]:
        """分页查询用户"""
        query = self.db.query(UserModel)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)

        if keyword:
            query = query.filter(
                or_(
                    UserModel.username.like(f"%{keyword}%"),
                    UserModel.nickname.like(f"%{keyword}%"),
                    UserModel.email.like(f"%{keyword}%")
                )
            )

        if department_id is not None:
            query = query.filter(UserModel.department_id == department_id)

        if status is not None:
            query = query.filter(UserModel.status == status)

        total = query.count()
        items = (
            query.order_by(UserModel.create_time.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return total, items
