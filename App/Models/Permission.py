"""Permission Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class PermissionModel(BaseModel):
    """权限模型"""

    __tablename__ = "sys_permission"
    __table_args__ = (
        Index('idx_permission_type', 'type'),
        Index('idx_permission_status', 'status'),
        Index('idx_perm_tenant_status', 'tenant_id', 'status'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(50), nullable=False, comment="权限名称")
    code = Column(String(50), unique=True, nullable=False, comment="权限编码")
    type = Column(Integer, nullable=False, comment="权限类型(0:菜单, 1:按钮, 2:API, 3:数据, 4:字段)")
    resource_type = Column(String(50), nullable=False, comment="资源类型")
    resource_id = Column(String(100), nullable=True, comment="资源ID")
    action = Column(String(20), nullable=False, comment="操作类型(view, create, update, delete, export)")
    path = Column(String(255), nullable=True, comment="访问路径(API路径或菜单路径)")
    method = Column(String(10), nullable=True, comment="请求方法(GET, POST, PUT, DELETE等)")
    parent_id = Column(Integer, ForeignKey("sys_permission.id"), nullable=True, comment="父权限ID")
    level = Column(Integer, default=1, comment="权限层级")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    description = Column(String(255), nullable=True, comment="权限描述")

    # 关系定义
    role_permissions = relationship("RolePermissionModel", back_populates="permission")
    menu_permissions = relationship("MenuPermissionModel", back_populates="permission")

    def __repr__(self):
        return f"<PermissionModel(name={self.name}, code={self.code})>"
