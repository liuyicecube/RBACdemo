"""Menu Service"""

from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from App.Models.Menu import MenuModel
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Repositories.MenuRepository import MenuRepository
from App.Utils.Validators import Validators
from App.Utils.Tree import TreeUtils
from App.Utils.Logger import logger
from App.Utils.Cache import cache
from App.Config.CacheKeys import MENU_TREE, USER_MENU_TREE, CACHE_EXPIRE_1_HOUR


class MenuService:
    """菜单服务类"""
    
    def __init__(self, db: Session):
        """初始化菜单服务"""
        self.db = db
        self.menu_repository = MenuRepository(db)
    
    def get_menu_by_id(self, menu_id: int, tenant_id: int) -> MenuModel:
        """根据ID获取菜单"""
        menu = self.menu_repository.get_by_id(menu_id, tenant_id=tenant_id)
        if not menu:
            raise NotFoundException(detail="菜单不存在")
        return menu
    
    def get_menu_by_code(self, code: str, tenant_id: int) -> MenuModel:
        """根据菜单编码获取菜单"""
        menu = self.menu_repository.get_by_code(code, tenant_id=tenant_id)
        if not menu:
            raise NotFoundException(detail="菜单不存在")
        return menu
    
    def get_menus(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[MenuModel]:
        """获取菜单列表"""
        return self.menu_repository.get_all(tenant_id=tenant_id, skip=skip, limit=limit)
    
    def get_active_menus(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[MenuModel]:
        """获取活跃菜单列表"""
        return self.menu_repository.get_active_menus(tenant_id=tenant_id, skip=skip, limit=limit)
    
    def get_menus_by_type(self, menu_type: int, tenant_id: int, skip: int = 0, limit: int = 100, include_all: bool = False) -> List[MenuModel]:
        """根据菜单类型获取菜单列表"""
        if not Validators.is_type_valid(menu_type, [0, 1, 2, 3, 4]) :
            raise ValidationException(detail="无效的菜单类型")
        
        return self.menu_repository.get_by_type(menu_type, tenant_id=tenant_id, skip=skip, limit=limit, include_all=include_all)
    
    def get_menus_by_parent_id(self, parent_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[MenuModel]:
        """根据父菜单ID获取子菜单列表"""
        if parent_id != 0:
            parent_menu = self.menu_repository.get_by_id(parent_id, tenant_id=tenant_id)
            if not parent_menu:
                raise NotFoundException(detail="父菜单不存在")
        
        return self.menu_repository.get_by_parent_id(parent_id, tenant_id=tenant_id, skip=skip, limit=limit)
    
    def get_root_menus(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[MenuModel]:
        """获取根菜单列表"""
        return self.menu_repository.get_root_menus(tenant_id=tenant_id, skip=skip, limit=limit)
    
    def search_menus(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100, include_all: bool = False) -> List[MenuModel]:
        """搜索菜单"""
        return self.menu_repository.search(keyword, tenant_id=tenant_id, skip=skip, limit=limit, include_all=include_all)
    
    def paginate_menus(
        self,
        tenant_id: int,
        keyword: str = None,
        menu_type: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[MenuModel]]:
        """分页查询菜单"""
        return self.menu_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            menu_type=menu_type,
            status=status,
            page=page,
            page_size=page_size
        )
    
    def create_menu(self, menu_data: Dict[str, Any], tenant_id: int, created_by: int) -> MenuModel:
        """创建菜单"""
        menu_type = menu_data.get("type")
        if not Validators.is_type_valid(menu_type, [0, 1, 2, 3, 4]) :
            raise ValidationException(detail="无效的菜单类型")
        
        code = menu_data.get("code")
        existing_menu = self.menu_repository.get_by_code(code, tenant_id=tenant_id)
        if existing_menu:
            raise ValidationException(detail="菜单编码已存在")
        
        name = menu_data.get("name")
        existing_menu = self.menu_repository.get_by_name(name, tenant_id=tenant_id)
        if existing_menu:
            raise ValidationException(detail="菜单名称已存在")
        
        parent_id = menu_data.get("parent_id")
        parent_level = 0
        if parent_id == 0 or parent_id is None:
            parent_id = None
            parent_level = 0
        else:
            parent_menu = self.menu_repository.get_by_id(parent_id, tenant_id=tenant_id)
            if not parent_menu:
                raise ValidationException(detail="父菜单不存在")
            parent_level = parent_menu.level
        
        menu = MenuModel(
            name=name,
            code=code,
            parent_id=parent_id,
            level=parent_level + 1,
            type=menu_type,
            path=menu_data.get("path"),
            component=menu_data.get("component"),
            icon=menu_data.get("icon"),
            sort=menu_data.get("sort", 0),
            status=menu_data.get("status", 1),
            tenant_id=tenant_id,
            created_by=created_by,
            updated_by=created_by
        )
        
        created_menu = self.menu_repository.create(menu)
        
        cache.delete(MENU_TREE)
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"创建菜单成功: {name}")
        
        return created_menu
    
    def update_menu(self, menu_id: int, menu_data: Dict[str, Any], tenant_id: int, updated_by: int) -> MenuModel:
        """更新菜单"""
        menu = self.menu_repository.get_by_id(menu_id, tenant_id=tenant_id)
        if not menu:
            raise NotFoundException(detail="菜单不存在")
        
        code = menu_data.get("code")
        if code and code != menu.code:
            existing_menu = self.menu_repository.get_by_code(code, tenant_id=tenant_id)
            if existing_menu:
                raise ValidationException(detail="菜单编码已存在")
            menu.code = code
        
        name = menu_data.get("name")
        if name and name != menu.name:
            existing_menu = self.menu_repository.get_by_name(name, tenant_id=tenant_id)
            if existing_menu:
                raise ValidationException(detail="菜单名称已存在")
            menu.name = name
        
        if "type" in menu_data and menu_data.get("type") is not None:
            menu_type = menu_data.get("type")
            if not Validators.is_type_valid(menu_type, [0, 1, 2, 3, 4]) :
                raise ValidationException(detail="无效的菜单类型")
            menu.type = menu_type
        
        if "parent_id" in menu_data:
            parent_id = menu_data.get("parent_id")
            if parent_id == 0 or parent_id is None:
                menu.parent_id = None
                menu.level = 1
            else:
                parent_menu = self.menu_repository.get_by_id(parent_id, tenant_id=tenant_id)
                if not parent_menu:
                    raise ValidationException(detail="父菜单不存在")
                if parent_id == menu_id:
                    raise ValidationException(detail="父菜单不能是自身")
                children_ids = self.menu_repository.get_menu_children_ids(menu_id, tenant_id=tenant_id)
                if parent_id in children_ids:
                    raise ValidationException(detail="存在循环依赖")
                menu.parent_id = parent_id
                menu.level = parent_menu.level + 1
        
        if "path" in menu_data:
            menu.path = menu_data.get("path")
        
        if "component" in menu_data:
            menu.component = menu_data.get("component")
        
        if "icon" in menu_data:
            menu.icon = menu_data.get("icon")
        
        if "sort" in menu_data:
            menu.sort = menu_data.get("sort")
        
        if "status" in menu_data:
            menu.status = menu_data.get("status")
        
        menu.updated_by = updated_by
        
        updated_menu = self.menu_repository.update(menu)
        
        cache.delete(MENU_TREE)
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"更新菜单成功: {menu.name}")
        
        return updated_menu
    
    def delete_menu(self, menu_id: int, tenant_id: int) -> bool:
        """删除菜单"""
        menu = self.menu_repository.get_by_id(menu_id, tenant_id=tenant_id)
        if not menu:
            raise NotFoundException(detail="菜单不存在")
        
        children_menus = self.menu_repository.get_by_parent_id(menu_id, tenant_id=tenant_id)
        if children_menus:
            raise ValidationException(detail="该菜单存在子菜单，无法删除")
        
        self.menu_repository.delete(menu)
        
        cache.delete(MENU_TREE)
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"删除菜单成功: {menu.name}")
        
        return True
    
    def update_menu_status(self, menu_id: int, status: int, tenant_id: int, updated_by: int) -> MenuModel:
        """更新菜单状态"""
        if not Validators.is_status_valid(status):
            raise ValidationException(detail="无效的状态值")
        
        menu = self.menu_repository.get_by_id(menu_id, tenant_id=tenant_id)
        if not menu:
            raise NotFoundException(detail="菜单不存在")
        
        menu.status = status
        menu.updated_by = updated_by
        
        updated_menu = self.menu_repository.update(menu)
        
        cache.delete(MENU_TREE)
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"更新菜单状态成功: {menu.name}, 状态: {status}")
        
        return updated_menu
    
    def get_menu_tree(self, tenant_id: int) -> List[Dict[str, Any]]:
        """获取菜单树形结构"""
        cache_key = MENU_TREE
        
        cached_tree = cache.get_json(cache_key)
        
        if cached_tree:
            return cached_tree
        
        menus = self.menu_repository.get_active_menus(tenant_id=tenant_id)
        
        menu_list = []
        for menu in menus:
            menu_list.append({
                "id": menu.id,
                "name": menu.name,
                "code": menu.code,
                "parent_id": menu.parent_id,
                "level": menu.level,
                "type": menu.type,
                "path": menu.path,
                "component": menu.component,
                "icon": menu.icon,
                "sort": menu.sort,
                "status": menu.status,
                "create_time": menu.create_time.isoformat() if menu.create_time else None,
                "update_time": menu.update_time.isoformat() if menu.update_time else None
            })
        
        tree = TreeUtils.build_tree(menu_list)
        sorted_tree = TreeUtils.sort_tree(tree, sort_key="sort")
        cache.set_json(cache_key, sorted_tree, expire=CACHE_EXPIRE_1_HOUR)
        
        return sorted_tree
    
    def get_user_menu_tree(self, user_id: int, tenant_id: int) -> List[Dict[str, Any]]:
        """获取用户菜单树形结构"""
        cache_key = USER_MENU_TREE.format(user_id=user_id)
        
        cached_tree = cache.get_json(cache_key)
        
        if cached_tree:
            return cached_tree
        
        from App.Repositories.UserRepository import UserRepository
        user_repository = UserRepository(self.db)
        user = user_repository.get_by_id(user_id, tenant_id=tenant_id)
        
        if user and user.username == 'admin':
            menus = self.menu_repository.get_active_menus(tenant_id=tenant_id)
            
            menu_list = []
            for menu in menus:
                menu_list.append({
                    "id": menu.id,
                    "name": menu.name,
                    "code": menu.code,
                    "parent_id": menu.parent_id,
                    "level": menu.level,
                    "type": menu.type,
                    "path": menu.path,
                    "component": menu.component,
                    "icon": menu.icon,
                    "sort": menu.sort,
                    "status": menu.status,
                    "create_time": menu.create_time.isoformat() if menu.create_time else None,
                    "update_time": menu.update_time.isoformat() if menu.update_time else None
                })
            
            tree = TreeUtils.build_tree(menu_list)
            sorted_tree = TreeUtils.sort_tree(tree, sort_key="sort")
            cache.set_json(cache_key, sorted_tree, expire=CACHE_EXPIRE_1_HOUR)
            
            return sorted_tree
        
        from App.Repositories.UserRoleRepository import UserRoleRepository
        user_role_repository = UserRoleRepository(self.db)
        user_roles = user_role_repository.get_by_user_id(user_id, tenant_id=tenant_id)
        
        if not user_roles:
            cache.set_json(cache_key, [], expire=CACHE_EXPIRE_1_HOUR)
            return []
        
        role_ids = [user_role.role_id for user_role in user_roles]
        
        from App.Repositories.RolePermissionRepository import RolePermissionRepository
        role_permission_repository = RolePermissionRepository(self.db)
        
        role_permissions = []
        for role_id in role_ids:
            role_permissions.extend(role_permission_repository.get_by_role_id(role_id, tenant_id=tenant_id))
        
        seen_permission_ids = set()
        unique_role_permissions = []
        for rp in role_permissions:
            if rp.permission_id not in seen_permission_ids:
                seen_permission_ids.add(rp.permission_id)
                unique_role_permissions.append(rp)
        
        role_permissions = unique_role_permissions
        
        permission_ids = [role_permission.permission_id for role_permission in role_permissions]
        
        from App.Repositories.PermissionRepository import PermissionRepository
        permission_repository = PermissionRepository(self.db)
        permissions = permission_repository.get_by_ids(permission_ids, tenant_id=tenant_id)
        
        menu_ids = []
        for permission in permissions:
            if permission.type == 0 or permission.type == 1:
                menu_code = permission.code.split(":")[0]
                menu = self.menu_repository.get_by_code(menu_code, tenant_id=tenant_id)
                if menu:
                    menu_ids.append(menu.id)
        
        all_menus = self.menu_repository.get_all(tenant_id=tenant_id)
        
        menu_map = {menu.id: menu for menu in all_menus}
        
        accessible_menu_ids = set()
        
        def _collect_menu_ids(menu_id):
            if menu_id not in accessible_menu_ids:
                accessible_menu_ids.add(menu_id)
                menu = menu_map.get(menu_id)
                if menu and menu.parent_id:
                    _collect_menu_ids(menu.parent_id)
        
        for menu_id in menu_ids:
            _collect_menu_ids(menu_id)
        
        user_menus = []
        for menu_id in accessible_menu_ids:
            menu = menu_map.get(menu_id)
            if menu and menu.status == 1:
                user_menus.append({
                    "id": menu.id,
                    "name": menu.name,
                    "code": menu.code,
                    "parent_id": menu.parent_id,
                    "level": menu.level,
                    "type": menu.type,
                    "path": menu.path,
                    "component": menu.component,
                    "icon": menu.icon,
                    "sort": menu.sort,
                    "status": menu.status,
                    "create_time": menu.create_time.isoformat() if menu.create_time else None,
                    "update_time": menu.update_time.isoformat() if menu.update_time else None
                })
        
        tree = TreeUtils.build_tree(user_menus)
        sorted_tree = TreeUtils.sort_tree(tree, sort_key="sort")
        cache.set_json(cache_key, sorted_tree, expire=CACHE_EXPIRE_1_HOUR)
        
        return sorted_tree
    
    def get_menu_children(self, menu_id: int, tenant_id: int) -> List[MenuModel]:
        """获取菜单的所有子菜单"""
        menu = self.menu_repository.get_by_id(menu_id, tenant_id=tenant_id)
        if not menu:
            raise NotFoundException(detail="菜单不存在")
        
        return self.menu_repository.get_by_parent_id(menu_id, tenant_id=tenant_id)
    
    def sort_menus(self, menu_ids: List[int], tenant_id: int) -> bool:
        """排序菜单"""
        for index, menu_id in enumerate(menu_ids):
            menu = self.menu_repository.get_by_id(menu_id, tenant_id=tenant_id)
            if menu:
                menu.sort = index
                self.menu_repository.update(menu)
        
        cache.delete(MENU_TREE)
        cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
        
        logger.info(f"排序菜单成功: {menu_ids}")
        
        return True
