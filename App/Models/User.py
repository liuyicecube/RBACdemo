"""User Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class UserModel(BaseModel):
    """用户模型"""

    __tablename__ = "sys_user"
    __table_args__ = (
        Index('idx_user_status', 'status'),
        Index('idx_user_department', 'department_id'),
        Index('idx_user_email', 'email'),
        Index('idx_user_phone', 'phone'),
        Index('idx_user_tenant_status', 'tenant_id', 'status'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="BCrypt加密的密码哈希")
    nickname = Column(String(50), nullable=False, comment="昵称")
    email = Column(String(100), nullable=True, index=True, comment="邮箱")
    phone = Column(String(20), nullable=True, index=True, comment="手机号")
    avatar = Column(String(255), nullable=True, comment="头像路径")
    department_id = Column(Integer, ForeignKey("sys_dept.id"), nullable=True, comment="所属部门ID")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    last_login_time = Column(DateTime, nullable=True, comment="最后登录时间")
    last_login_ip = Column(String(50), nullable=True, comment="最后登录IP")

    # 关系定义
    department = relationship("DepartmentModel", back_populates="users", foreign_keys=[department_id])
    user_roles = relationship("UserRoleModel", back_populates="user")
    user_group_relations = relationship("UserGroupRelationModel", back_populates="user")
    profile = relationship("UserProfileModel", uselist=False, back_populates="user")

    def __repr__(self):
        return f"<UserModel(username={self.username}, nickname={self.nickname})>"
