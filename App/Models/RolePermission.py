"""Role Permission Model"""

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class RolePermissionModel(BaseModel):
    """角色权限关联模型"""

    __tablename__ = "sys_role_permission"
    __table_args__ = (
        UniqueConstraint('role_id', 'permission_id', name='uk_role_permission'),
        Index('idx_role_permission_role', 'role_id'),
        Index('idx_role_permission_permission', 'permission_id'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    role_id = Column(Integer, ForeignKey("sys_role.id"), nullable=False, comment="角色ID")
    permission_id = Column(Integer, ForeignKey("sys_permission.id"), nullable=False, comment="权限ID")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")

    # 关系定义
    role = relationship("RoleModel", back_populates="role_permissions")
    permission = relationship("PermissionModel", back_populates="role_permissions")

    def __repr__(self):
        return f"<RolePermissionModel(role_id={self.role_id}, permission_id={self.permission_id})>"
