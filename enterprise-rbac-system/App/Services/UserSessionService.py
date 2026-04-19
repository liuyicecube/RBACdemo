"""User Session Service"""

from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from datetime import datetime
from App.Models.UserSession import UserSessionModel
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Repositories.UserSessionRepository import UserSessionRepository
from App.Utils.Logger import logger
from App.Utils.Cache import cache


class UserSessionService:
    """用户会话服务类"""

    def __init__(self, db: Session):
        """初始化用户会话服务"""
        self.db = db
        self.user_session_repository = UserSessionRepository(db)
        from App.Repositories.UserRepository import UserRepository
        self.user_repository = UserRepository(db)

    def get_session_by_id(self, session_id: int, tenant_id: int) -> UserSessionModel:
        """根据ID获取用户会话"""
        session = self.user_session_repository.get_by_id(session_id, tenant_id=tenant_id)
        if not session:
            raise NotFoundException(detail="用户会话不存在")
        return session

    def get_session_by_session_id(self, session_id: str, tenant_id: int) -> UserSessionModel:
        """根据会话ID获取用户会话"""
        session = self.user_session_repository.get_by_session_id(session_id, tenant_id=tenant_id)
        if not session:
            raise NotFoundException(detail="用户会话不存在")
        return session

    def get_session_by_access_token(self, access_token: str, tenant_id: int) -> UserSessionModel:
        """根据访问令牌获取用户会话"""
        session = self.user_session_repository.get_by_access_token(access_token, tenant_id=tenant_id)
        if not session:
            raise NotFoundException(detail="用户会话不存在")
        return session

    def get_sessions_by_user_id(self, user_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """根据用户ID获取用户会话列表"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        return self.user_session_repository.get_by_user_id(user_id, tenant_id=tenant_id, skip=skip, limit=limit)

    def get_active_sessions_by_user_id(self, user_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """根据用户ID获取活跃用户会话列表"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        return self.user_session_repository.get_active_sessions_by_user_id(user_id, tenant_id=tenant_id, skip=skip, limit=limit)

    def get_all_active_sessions(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """获取所有活跃用户会话"""
        return self.user_session_repository.get_all_active_sessions(tenant_id=tenant_id, skip=skip, limit=limit)

    def get_expired_sessions(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """获取过期用户会话"""
        return self.user_session_repository.get_expired_sessions(tenant_id=tenant_id, skip=skip, limit=limit)

    def search_sessions(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserSessionModel]:
        """搜索用户会话"""
        return self.user_session_repository.search(keyword, tenant_id=tenant_id, skip=skip, limit=limit)

    def paginate_sessions(
        self,
        tenant_id: int,
        user_id: int = None,
        device_type: str = None,
        status: int = None,
        keyword: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[UserSessionModel]]:
        """分页查询用户会话"""
        return self.user_session_repository.paginate(
            tenant_id=tenant_id,
            user_id=user_id,
            device_type=device_type,
            status=status,
            keyword=keyword,
            page=page,
            page_size=page_size
        )

    def create_session(self, session_data: Dict[str, Any], tenant_id: int, created_by: int) -> UserSessionModel:
        """创建用户会话"""
        user_id = session_data.get("user_id")
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        session_id = session_data.get("session_id")
        existing_session = self.user_session_repository.get_by_session_id(session_id, tenant_id=tenant_id)
        if existing_session:
            raise ValidationException(detail="会话ID已存在")

        session = UserSessionModel(
            user_id=user_id,
            session_id=session_id,
            access_token=session_data.get("access_token"),
            refresh_token=session_data.get("refresh_token"),
            device_type=session_data.get("device_type"),
            device_info=session_data.get("device_info"),
            os_info=session_data.get("os_info"),
            browser_info=session_data.get("browser_info"),
            ip_address=session_data.get("ip_address"),
            login_time=session_data.get("login_time"),
            last_active_time=session_data.get("last_active_time"),
            expire_time=session_data.get("expire_time"),
            status=1,
            tenant_id=tenant_id,
            created_by=created_by,
            updated_by=created_by
        )

        created_session = self.user_session_repository.create(session)

        logger.info(f"创建用户会话成功: 用户ID={user_id}, 会话ID={session_id}")

        return created_session

    def update_session(self, session_id: int, session_data: Dict[str, Any], tenant_id: int, updated_by: int) -> UserSessionModel:
        """更新用户会话"""
        session = self.user_session_repository.get_by_id(session_id, tenant_id=tenant_id)
        if not session:
            raise NotFoundException(detail="用户会话不存在")

        if "access_token" in session_data:
            session.access_token = session_data.get("access_token")

        if "refresh_token" in session_data:
            session.refresh_token = session_data.get("refresh_token")

        if "last_active_time" in session_data:
            session.last_active_time = session_data.get("last_active_time")

        if "expire_time" in session_data:
            session.expire_time = session_data.get("expire_time")

        if "status" in session_data:
            session.status = session_data.get("status")

        session.updated_by = updated_by

        updated_session = self.user_session_repository.update(session)

        logger.info(f"更新用户会话成功: 会话ID={session.session_id}")

        return updated_session

    def update_last_active(self, session_id: int, tenant_id: int) -> UserSessionModel:
        """更新会话最后活跃时间"""
        session = self.user_session_repository.get_by_id(session_id, tenant_id=tenant_id)
        if not session:
            raise NotFoundException(detail="用户会话不存在")

        session.last_active_time = datetime.now()
        session.updated_by = session.updated_by

        updated_session = self.user_session_repository.update(session)

        return updated_session

    def delete_session(self, session_id: int, tenant_id: int) -> bool:
        """删除用户会话"""
        session = self.user_session_repository.get_by_id(session_id, tenant_id=tenant_id)
        if not session:
            raise NotFoundException(detail="用户会话不存在")

        self.user_session_repository.delete(session)

        logger.info(f"删除用户会话成功: 会话ID={session.session_id}")

        return True

    def kick_user(self, session_ids: List[int], tenant_id: int) -> Dict[str, int]:
        """踢人下线"""
        success_count = 0
        failed_count = 0

        for session_id in session_ids:
            try:
                session = self.user_session_repository.get_by_id(session_id, tenant_id=tenant_id)
                if session:
                    self.user_session_repository.expire_session(session_id, tenant_id=tenant_id)
                    success_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                logger.error(f"踢人下线失败: 会话ID={session_id}, 错误={str(e)}")
                failed_count += 1

        cache.delete_pattern(f"user:session:*")

        logger.info(f"踢人下线完成: 成功={success_count}, 失败={failed_count}")

        return {
            "success_count": success_count,
            "failed_count": failed_count
        }

    def kick_all_user_sessions(self, user_id: int, tenant_id: int) -> int:
        """踢用户所有会话下线"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        count = self.user_session_repository.expire_by_user_id(user_id, tenant_id=tenant_id)

        cache.delete_pattern(f"user:session:*")

        logger.info(f"踢用户所有会话下线: 用户ID={user_id}, 会话数={count}")

        return count

    def count_expired_sessions(self, tenant_id: int) -> dict:
        """统计过期会话数量"""
        result = self.user_session_repository.count_expired_sessions(tenant_id=tenant_id)

        logger.info(f"统计过期会话: {result}")

        return result

    def clean_expired_sessions(self, tenant_id: int) -> dict:
        """清理过期会话"""
        result = self.user_session_repository.clean_expired_sessions(tenant_id=tenant_id)

        logger.info(f"清理过期会话: {result}")

        return result
