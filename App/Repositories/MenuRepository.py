"""Menu Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from App.Models.Menu import MenuModel
from App.Repositories.Base import BaseRepository


class MenuRepository(BaseRepository[MenuModel]):
    """菜单仓储类"""
    
    def __init__(self, db: Session):
        """初始化菜单仓储"""
        super().__init__(db, MenuModel)
    
    def get_by_code(self, code: str, tenant_id: int) -> Optional[MenuModel]:
        """根据菜单编码获取菜单"""
        return self.db.query(MenuModel).filter(
            MenuModel.code == code,
            MenuModel.tenant_id == tenant_id,
            MenuModel.is_deleted == 0
        ).first()
    
    def get_by_name(self, name: str, tenant_id: int) -> Optional[MenuModel]:
        """根据菜单名称获取菜单"""
        return self.db.query(MenuModel).filter(
            MenuModel.name == name,
            MenuModel.tenant_id == tenant_id,
            MenuModel.is_deleted == 0
        ).first()
    
    def get_by_type(self, menu_type: int, tenant_id: int, skip: int = 0, limit: int = 100, include_all: bool = False) -> List[MenuModel]:
        """根据菜单类型获取菜单"""
        query = self.db.query(MenuModel).filter(
            MenuModel.type == menu_type,
            MenuModel.tenant_id == tenant_id,
            MenuModel.is_deleted == 0
        )
        if not include_all:
            query = query.filter(MenuModel.status == 1)
        return query.order_by(MenuModel.sort).offset(skip).limit(limit).all()
    
    def get_by_parent_id(self, parent_id: int, tenant_id: int, skip: int = 0, limit: int = 100, include_all: bool = False) -> List[MenuModel]:
        """根据父菜单ID获取子菜单"""
        query = self.db.query(MenuModel).filter(
            MenuModel.parent_id == parent_id,
            MenuModel.tenant_id == tenant_id,
            MenuModel.is_deleted == 0
        )
        if not include_all:
            query = query.filter(MenuModel.status == 1)
        return query.order_by(MenuModel.sort).offset(skip).limit(limit).all()
    
    def get_root_menus(self, tenant_id: int, skip: int = 0, limit: int = 100, include_all: bool = False) -> List[MenuModel]:
        """获取根菜单"""
        query = self.db.query(MenuModel).filter(
            (MenuModel.parent_id == None) | (MenuModel.parent_id == 0),
            MenuModel.tenant_id == tenant_id,
            MenuModel.is_deleted == 0
        )
        if not include_all:
            query = query.filter(MenuModel.status == 1)
        return query.order_by(MenuModel.sort).offset(skip).limit(limit).all()
    
    def search(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100, include_all: bool = False) -> List[MenuModel]:
        """搜索菜单"""
        query = self.db.query(MenuModel).filter(
            or_(
                MenuModel.name.like(f"%{keyword}%"),
                MenuModel.code.like(f"%{keyword}%"),
                MenuModel.path.like(f"%{keyword}%")
            ),
            MenuModel.tenant_id == tenant_id,
            MenuModel.is_deleted == 0
        )
        if not include_all:
            query = query.filter(MenuModel.status == 1)
        return query.order_by(MenuModel.sort).offset(skip).limit(limit).all()
    
    def get_active_menus(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[MenuModel]:
        """获取活跃菜单"""
        return self.db.query(MenuModel).filter(
            MenuModel.tenant_id == tenant_id,
            MenuModel.is_deleted == 0,
            MenuModel.status == 1
        ).order_by(MenuModel.sort).offset(skip).limit(limit).all()
    
    def get_all_menus(self, tenant_id: int, include_all: bool = False) -> List[MenuModel]:
        """获取所有菜单"""
        query = self.db.query(MenuModel).filter(
            MenuModel.tenant_id == tenant_id,
            MenuModel.is_deleted == 0
        )
        if not include_all:
            query = query.filter(MenuModel.status == 1)
        return query.order_by(MenuModel.sort).all()
    
    def get_menu_children_ids(self, menu_id: int, tenant_id: int) -> List[int]:
        """获取菜单的所有子菜单ID"""
        # 递归获取所有子菜单ID
        def _get_children_ids(mid: int) -> List[int]:
            children = self.db.query(MenuModel.id).filter(
                MenuModel.parent_id == mid,
                MenuModel.tenant_id == tenant_id,
                MenuModel.is_deleted == 0
            ).all()
            children_ids = [child.id for child in children]
            for child_id in children_ids:
                children_ids.extend(_get_children_ids(child_id))
            return children_ids
        
        return _get_children_ids(menu_id)
    
    def paginate(
        self,
        tenant_id: int,
        keyword: str = None,
        menu_type: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[MenuModel]]:
        """分页查询菜单"""
        query = self.db.query(MenuModel).filter(
            MenuModel.tenant_id == tenant_id,
            MenuModel.is_deleted == 0
        )
        
        if keyword:
            query = query.filter(
                or_(
                    MenuModel.name.like(f"%{keyword}%"),
                    MenuModel.code.like(f"%{keyword}%")
                )
            )
        
        if menu_type is not None:
            query = query.filter(MenuModel.type == menu_type)
        
        if status is not None:
            query = query.filter(MenuModel.status == status)
        
        total = query.count()
        items = query.order_by(MenuModel.sort, MenuModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()
        
        return total, items