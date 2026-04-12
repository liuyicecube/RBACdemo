"""System Config Model"""

from sqlalchemy import Column, String, Integer, Text, Index
from App.Models.Base import BaseModel


class SystemConfigModel(BaseModel):
    """系统配置模型"""

    __tablename__ = "sys_config"
    __table_args__ = (
        Index('idx_config_key', 'config_key'),
        Index('idx_config_group', 'group_name'),
        Index('idx_config_status', 'status'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    config_key = Column(String(100), unique=True, nullable=False, index=True, comment="配置键")
    config_value = Column(Text, nullable=True, comment="配置值")
    config_type = Column(String(20), default="string", comment="配置类型(string,int,bool,json)")
    description = Column(String(255), nullable=True, comment="配置描述")
    group_name = Column(String(50), nullable=True, comment="配置分组")
    is_system = Column(Integer, default=0, comment="是否系统配置(0:否,1:是)")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    sort = Column(Integer, default=0, comment="排序")

    def __repr__(self):
        return f"<SystemConfigModel(key={self.config_key}, value={self.config_value})>"
