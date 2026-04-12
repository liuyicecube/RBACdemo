"""Menu Permission Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from App.Models.MenuPermission import MenuPermissionModel
from App.Repositories.Base import BaseRepository


class MenuPermissionRepository(BaseRepository[MenuPermissionModel]):
    """菜单权限关联仓储类"""

    def __init__(self, db: Session):
        """初始化菜单权限关联仓储"""
        super().__init__(db, MenuPermissionModel)

    def get_by_menu_id(self, menu_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[MenuPermissionModel]:
        """根据菜单ID获取关联权限"""
        return self.db.query(MenuPermissionModel).filter(
            MenuPermissionModel.menu_id == menu_id,
            MenuPermissionModel.tenant_id == tenant_id,
            MenuPermissionModel.is_deleted == 0,
            MenuPermissionModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_by_permission_id(self, permission_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[MenuPermissionModel]:
        """根据权限ID获取关联菜单"""
        return self.db.query(MenuPermissionModel).filter(
            MenuPermissionModel.permission_id == permission_id,
            MenuPermissionModel.tenant_id == tenant_id,
            MenuPermissionModel.is_deleted == 0,
            MenuPermissionModel.status == 1
        ).offset(skip).limit(limit).all()

    def delete_by_menu_id(self, menu_id: int, tenant_id: int) -> None:
        """根据菜单ID删除所有关联权限"""
        self.db.query(MenuPermissionModel).filter(
            MenuPermissionModel.menu_id == menu_id,
            MenuPermissionModel.tenant_id == tenant_id
        ).delete()
        self.db.commit()

    def delete_by_permission_id(self, permission_id: int, tenant_id: int) -> None:
        """根据权限ID删除所有关联菜单"""
        self.db.query(MenuPermissionModel).filter(
            MenuPermissionModel.permission_id == permission_id,
            MenuPermissionModel.tenant_id == tenant_id
        ).delete()
        self.db.commit()
