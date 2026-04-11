"""User Group Role Relation Model"""

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class UserGroupRoleRelationModel(BaseModel):
    """用户组-角色关联模型"""
    
    __tablename__ = "sys_user_group_role_relation"
    __table_args__ = (
        UniqueConstraint('user_group_id', 'role_id', name='uk_user_group_role'),
        Index('idx_ugrr_user_group', 'user_group_id'),
        Index('idx_ugrr_role', 'role_id'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_group_id = Column(Integer, ForeignKey("sys_user_group.id"), nullable=False, comment="用户组ID")
    role_id = Column(Integer, ForeignKey("sys_role.id"), nullable=False, comment="角色ID")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    
    user_group = relationship("UserGroupModel", back_populates="role_relations")
    role = relationship("RoleModel", back_populates="user_group_role_relations")
    
    def __repr__(self):
        return f"<UserGroupRoleRelationModel(group_id={self.user_group_id}, role_id={self.role_id})>"
