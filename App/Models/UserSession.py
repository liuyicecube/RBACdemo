"""User Session Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class UserSessionModel(BaseModel):
    """用户会话模型"""

    __tablename__ = "sys_user_session"
    __table_args__ = (
        Index('idx_session_user', 'user_id'),
        Index('idx_session_status', 'status'),
        Index('idx_session_expire', 'expire_time'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="用户ID")
    session_id = Column(String(100), unique=True, nullable=False, index=True, comment="会话ID")
    access_token = Column(String(500), nullable=False, comment="访问令牌")
    refresh_token = Column(String(500), nullable=True, comment="刷新令牌")
    device_type = Column(String(50), nullable=True, comment="设备类型")
    device_info = Column(String(500), nullable=True, comment="设备信息")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    login_time = Column(DateTime, nullable=False, comment="登录时间")
    last_active_time = Column(DateTime, nullable=False, comment="最后活跃时间")
    expire_time = Column(DateTime, nullable=False, comment="过期时间")
    status = Column(Integer, default=1, comment="状态(0:已失效,1:有效)")

    def __repr__(self):
        return f"<UserSessionModel(user_id={self.user_id}, session_id={self.session_id})>"
