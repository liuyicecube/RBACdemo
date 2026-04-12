"""User Session Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from App.Models.UserSession import UserSessionModel
from App.Repositories.Base import BaseRepository


class UserSessionRepository(BaseRepository[UserSessionModel]):
    """用户会话仓储类"""

    def __init__(self, db: Session):
        """初始化用户会话仓储"""
        super().__init__(db, UserSessionModel)

    def get_by_session_id(self, session_id: str, tenant_id: int) -> Optional[UserSessionModel]:
        """根据会话ID获取用户会话"""
        return self.db.query(UserSessionModel).filter(
            UserSessionModel.session_id == session_id,
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0
        ).first()

    def get_by_access_token(self, access_token: str, tenant_id: int) -> Optional[UserSessionModel]:
        """根据访问令牌获取用户会话"""
        return self.db.query(UserSessionModel).filter(
            UserSessionModel.access_token == access_token,
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0
        ).first()

    def get_by_user_id(self, user_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """根据用户ID获取用户会话列表"""
        return self.db.query(UserSessionModel).filter(
            UserSessionModel.user_id == user_id,
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0
        ).order_by(UserSessionModel.last_active_time.desc()).offset(skip).limit(limit).all()

    def get_active_sessions_by_user_id(self, user_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """根据用户ID获取活跃用户会话列表"""
        return self.db.query(UserSessionModel).filter(
            UserSessionModel.user_id == user_id,
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0,
            UserSessionModel.status == 1,
            UserSessionModel.expire_time > datetime.now()
        ).order_by(UserSessionModel.last_active_time.desc()).offset(skip).limit(limit).all()

    def get_all_active_sessions(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """获取所有活跃用户会话"""
        return self.db.query(UserSessionModel).filter(
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0,
            UserSessionModel.status == 1,
            UserSessionModel.expire_time > datetime.now()
        ).order_by(UserSessionModel.last_active_time.desc()).offset(skip).limit(limit).all()

    def get_expired_sessions(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """获取过期用户会话"""
        return self.db.query(UserSessionModel).filter(
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0,
            or_(
                UserSessionModel.status == 0,
                UserSessionModel.expire_time <= datetime.now()
            )
        ).order_by(UserSessionModel.expire_time).offset(skip).limit(limit).all()

    def get_by_device_type(self, device_type: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """根据设备类型获取用户会话"""
        return self.db.query(UserSessionModel).filter(
            UserSessionModel.device_type == device_type,
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0
        ).offset(skip).limit(limit).all()

    def search(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """搜索用户会话"""
        return self.db.query(UserSessionModel).filter(
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0,
            or_(
                UserSessionModel.session_id.like(f"%{keyword}%"),
                UserSessionModel.device_type.like(f"%{keyword}%"),
                UserSessionModel.device_info.like(f"%{keyword}%"),
                UserSessionModel.ip_address.like(f"%{keyword}%")
            )
        ).order_by(UserSessionModel.last_active_time.desc()).offset(skip).limit(limit).all()

    def delete_by_user_id(self, user_id: int, tenant_id: int) -> int:
        """根据用户ID删除用户会话"""
        from App.Models.UserSession import UserSessionModel
        updated = self.db.query(UserSessionModel).filter(
            UserSessionModel.user_id == user_id,
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0
        ).update({"is_deleted": 1})
        self.db.commit()
        return updated

    def expire_by_user_id(self, user_id: int, tenant_id: int) -> int:
        """根据用户ID强制过期用户会话"""
        from App.Models.UserSession import UserSessionModel
        updated = self.db.query(UserSessionModel).filter(
            UserSessionModel.user_id == user_id,
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0,
            UserSessionModel.status == 1
        ).update({"status": 0})
        self.db.commit()
        return updated

    def expire_session(self, session_id: int, tenant_id: int) -> Optional[UserSessionModel]:
        """强制过期单个会话"""
        session = self.get_by_id(session_id, tenant_id=tenant_id)
        if session:
            session.status = 0
            self.update(session)
        return session

    def clean_expired_sessions(self, tenant_id: int) -> int:
        """清理过期会话"""
        from App.Models.UserSession import UserSessionModel
        updated = self.db.query(UserSessionModel).filter(
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0,
            UserSessionModel.expire_time <= datetime.now()
        ).update({"is_deleted": 1})
        self.db.commit()
        return updated

    def paginate(
        self,
        tenant_id: int,
        user_id: int = None,
        device_type: str = None,
        status: int = None,
        keyword: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[UserSessionModel]]:
        """分页查询用户会话"""
        query = self.db.query(UserSessionModel).filter(
            UserSessionModel.tenant_id == tenant_id,
            UserSessionModel.is_deleted == 0
        )

        if user_id is not None:
            query = query.filter(UserSessionModel.user_id == user_id)

        if device_type:
            query = query.filter(UserSessionModel.device_type == device_type)

        if status is not None:
            query = query.filter(UserSessionModel.status == status)

        if keyword:
            query = query.filter(
                or_(
                    UserSessionModel.session_id.like(f"%{keyword}%"),
                    UserSessionModel.device_type.like(f"%{keyword}%"),
                    UserSessionModel.device_info.like(f"%{keyword}%"),
                    UserSessionModel.ip_address.like(f"%{keyword}%")
                )
            )

        total = query.count()
        items = query.order_by(UserSessionModel.last_active_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return total, items
