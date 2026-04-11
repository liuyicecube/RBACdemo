"""System Dict Item Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class SystemDictItemModel(BaseModel):
    """系统字典项模型"""
    
    __tablename__ = "sys_dict_item"
    __table_args__ = (
        UniqueConstraint('dict_id', 'value', name='uk_dict_value'),
        Index('idx_dict_item_dict', 'dict_id'),
        Index('idx_dict_item_status', 'status'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    dict_id = Column(Integer, ForeignKey("sys_dict.id"), nullable=False, comment="字典ID")
    label = Column(String(100), nullable=False, comment="标签")
    value = Column(String(100), nullable=False, comment="值")
    color = Column(String(50), nullable=True, comment="颜色")
    description = Column(String(500), nullable=True, comment="描述")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    sort = Column(Integer, default=0, comment="排序")
    
    dict = relationship("SystemDictModel", back_populates="items")
    
    def __repr__(self):
        return f"<SystemDictItemModel(label={self.label}, value={self.value})>"
