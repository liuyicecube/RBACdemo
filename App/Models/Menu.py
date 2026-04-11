"""Menu Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class MenuModel(BaseModel):
    """菜单模型"""
    
    __tablename__ = "sys_menu"
    __table_args__ = (
        Index('idx_menu_parent', 'parent_id'),
        Index('idx_menu_sort', 'sort'),
        Index('idx_menu_tenant_status', 'tenant_id', 'status'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(50), nullable=False, comment="菜单名称")
    code = Column(String(50), unique=True, nullable=False, comment="菜单编码")
    parent_id = Column(Integer, ForeignKey("sys_menu.id"), nullable=True, comment="父菜单ID")
    level = Column(Integer, default=1, comment="菜单层级")
    type = Column(Integer, nullable=False, comment="菜单类型(0:目录,1:菜单,2:按钮,3:内嵌,4:外链)")
    path = Column(String(255), nullable=True, comment="访问路径")
    component = Column(String(255), nullable=True, comment="组件路径")
    icon = Column(String(50), nullable=True, comment="菜单图标")
    sort = Column(Integer, default=0, comment="排序")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    
    # 关系定义
    menu_permissions = relationship("MenuPermissionModel", back_populates="menu")
    
    def __repr__(self):
        return f"<MenuModel(name={self.name}, code={self.code})>"