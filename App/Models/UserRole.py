"""User Role Model"""

from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class UserRoleModel(BaseModel):
    """用户角色关联模型"""
    
    __tablename__ = "sys_user_role"
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id', name='uk_user_role'),
        Index('idx_user_role_user', 'user_id'),
        Index('idx_user_role_role', 'role_id'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="用户ID")
    role_id = Column(Integer, ForeignKey("sys_role.id"), nullable=False, comment="角色ID")
    is_primary = Column(Boolean, default=False, comment="是否主角色")
    effective_time = Column(DateTime, nullable=True, comment="生效时间")
    expire_time = Column(DateTime, nullable=True, comment="过期时间")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    
    # 关系定义
    user = relationship("UserModel", back_populates="user_roles")
    role = relationship("RoleModel", back_populates="user_roles")
    
    def __repr__(self):
        return f"<UserRoleModel(user_id={self.user_id}, role_id={self.role_id})>"