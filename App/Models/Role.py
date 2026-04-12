"""Role Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class RoleModel(BaseModel):
    """角色模型"""

    __tablename__ = "sys_role"
    __table_args__ = (
        Index('idx_role_status', 'status'),
        Index('idx_role_parent', 'parent_id'),
        Index('idx_role_type', 'type'),
        Index('idx_role_tenant_status', 'tenant_id', 'status'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(50), unique=True, nullable=False, comment="角色名称")
    code = Column(String(50), unique=True, nullable=False, comment="角色编码")
    parent_id = Column(Integer, ForeignKey("sys_role.id"), nullable=True, comment="父角色ID")
    level = Column(Integer, default=1, comment="角色层级")
    type = Column(Integer, default=3, comment="角色类型(0:系统角色, 1:功能角色, 2:数据角色, 3:自定义角色)")
    data_scope = Column(Integer, default=0, comment="数据范围(0:全部,1:本部门,2:本部门及下级,3:仅本人,4:自定义)")
    sort = Column(Integer, default=0, comment="排序")
    description = Column(String(255), nullable=True, comment="角色描述")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")

    # 关系定义
    user_roles = relationship("UserRoleModel", back_populates="role")
    role_permissions = relationship("RolePermissionModel", back_populates="role")
    user_group_role_relations = relationship("UserGroupRoleRelationModel", back_populates="role")

    def __repr__(self):
        return f"<RoleModel(name={self.name}, code={self.code})>"
