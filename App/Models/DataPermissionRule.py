"""Data Permission Rule Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class DataPermissionRuleModel(BaseModel):
    """数据权限规则模型"""
    
    __tablename__ = "sys_data_permission_rule"
    __table_args__ = (
        Index('idx_data_perm_permission', 'permission_id'),
        Index('idx_data_perm_status', 'status'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(100), nullable=False, comment="规则名称")
    code = Column(String(100), unique=True, nullable=False, comment="规则编码")
    permission_id = Column(Integer, ForeignKey("sys_permission.id"), nullable=False, comment="关联权限ID")
    resource_table = Column(String(100), nullable=False, comment="资源表名")
    rule_type = Column(Integer, nullable=False, comment="规则类型(0:全部,1:本部门,2:本部门及下级,3:仅本人,4:自定义)")
    rule_expression = Column(Text, nullable=True, comment="自定义规则表达式(SQL WHERE片段)")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    description = Column(String(500), nullable=True, comment="规则描述")
    
    # 关系定义
    permission = relationship("PermissionModel")
    
    def __repr__(self):
        return f"<DataPermissionRuleModel(name={self.name}, code={self.code})>"
