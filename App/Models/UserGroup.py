"""User Group Model"""

from sqlalchemy import Column, String, Integer, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class UserGroupModel(BaseModel):
    """用户组模型"""

    __tablename__ = "sys_user_group"
    __table_args__ = (
        Index('idx_user_group_status', 'status'),
        Index('idx_user_group_code', 'code'),
        Index('idx_ug_tenant_status', 'tenant_id', 'status'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(100), nullable=False, comment="用户组名称")
    code = Column(String(100), unique=True, nullable=False, index=True, comment="用户组编码")
    description = Column(String(500), nullable=True, comment="描述")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    sort = Column(Integer, default=0, comment="排序")

    user_relations = relationship("UserGroupRelationModel", back_populates="user_group")
    role_relations = relationship("UserGroupRoleRelationModel", back_populates="user_group")

    def __repr__(self):
        return f"<UserGroupModel(name={self.name}, code={self.code})>"
