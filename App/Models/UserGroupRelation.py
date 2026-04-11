"""User Group Relation Model"""

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class UserGroupRelationModel(BaseModel):
    """用户组-用户关联模型"""
    
    __tablename__ = "sys_user_group_relation"
    __table_args__ = (
        UniqueConstraint('user_group_id', 'user_id', name='uk_user_group_user'),
        Index('idx_ugr_user_group', 'user_group_id'),
        Index('idx_ugr_user', 'user_id'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_group_id = Column(Integer, ForeignKey("sys_user_group.id"), nullable=False, comment="用户组ID")
    user_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="用户ID")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    
    user_group = relationship("UserGroupModel", back_populates="user_relations")
    user = relationship("UserModel", back_populates="user_group_relations")
    
    def __repr__(self):
        return f"<UserGroupRelationModel(group_id={self.user_group_id}, user_id={self.user_id})>"
