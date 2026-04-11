"""Base Model"""

from sqlalchemy import Column, Integer, DateTime, Index
from sqlalchemy.sql import func
from App.Config.Database import Base


class BaseModel(Base):
    """基础模型类，包含公共字段（除id外，id需要在每个模型中单独定义以确保顺序）"""
    
    __abstract__ = True
    __table_args__ = (
        Index('idx_tenant_id', 'tenant_id'),
        Index('idx_is_deleted', 'is_deleted'),
        Index('idx_create_time', 'create_time'),
        Index('idx_update_time', 'update_time'),
        Index('idx_tenant_deleted', 'tenant_id', 'is_deleted'),
    )
    
    tenant_id = Column(Integer, nullable=True, comment="租户ID")
    create_time = Column(DateTime, default=func.now(), nullable=False, comment="创建时间")
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    delete_time = Column(DateTime, nullable=True, comment="删除时间")
    created_by = Column(Integer, nullable=True, comment="创建人ID")
    updated_by = Column(Integer, nullable=True, comment="更新人ID")
    deleted_by = Column(Integer, nullable=True, comment="删除人ID")
    is_deleted = Column(Integer, default=0, nullable=False, comment="是否删除(0:未删除,1:已删除)")
    version = Column(Integer, default=1, nullable=False, comment="版本号(乐观锁)")