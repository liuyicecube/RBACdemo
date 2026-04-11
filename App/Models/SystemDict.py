"""System Dict Model"""

from sqlalchemy import Column, String, Integer, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class SystemDictModel(BaseModel):
    """系统字典模型"""
    
    __tablename__ = "sys_dict"
    __table_args__ = (
        Index('idx_dict_status', 'status'),
        Index('idx_dict_code', 'code'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(100), nullable=False, comment="字典名称")
    code = Column(String(100), unique=True, nullable=False, index=True, comment="字典编码")
    description = Column(String(500), nullable=True, comment="描述")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    sort = Column(Integer, default=0, comment="排序")
    
    items = relationship("SystemDictItemModel", back_populates="dict")
    
    def __repr__(self):
        return f"<SystemDictModel(name={self.name}, code={self.code})>"
