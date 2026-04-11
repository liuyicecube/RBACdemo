"""Menu Permission Model"""

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class MenuPermissionModel(BaseModel):
    """菜单权限关联模型"""
    
    __tablename__ = "sys_menu_permission"
    __table_args__ = (
        UniqueConstraint('menu_id', 'permission_id', name='uk_menu_permission'),
        Index('idx_menu_perm_menu', 'menu_id'),
        Index('idx_menu_perm_permission', 'permission_id'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    menu_id = Column(Integer, ForeignKey("sys_menu.id"), nullable=False, comment="菜单ID")
    permission_id = Column(Integer, ForeignKey("sys_permission.id"), nullable=False, comment="权限ID")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
    
    menu = relationship("MenuModel", back_populates="menu_permissions")
    permission = relationship("PermissionModel", back_populates="menu_permissions")
    
    def __repr__(self):
        return f"<MenuPermissionModel(menu_id={self.menu_id}, permission_id={self.permission_id})>"
