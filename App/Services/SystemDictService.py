"""System Dict Service"""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from App.Models.SystemDict import SystemDictModel
from App.Models.SystemDictItem import SystemDictItemModel
from App.Repositories.SystemDictRepository import SystemDictRepository, SystemDictItemRepository
from App.Schemas.SystemDict import (
    SystemDictCreate,
    SystemDictUpdate,
    SystemDictResponse,
    SystemDictWithItemsResponse,
    SystemDictItemCreate,
    SystemDictItemUpdate,
    SystemDictItemResponse
)
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Utils.Cache import cache
from App.Config.CacheKeys import (
    SYSTEM_DICT_ALL,
    SYSTEM_DICT_BY_CODE,
    SYSTEM_DICT_ITEMS_BY_CODE,
    CACHE_EXPIRE_1_HOUR,
    CACHE_EXPIRE_5_MINUTES
)


class SystemDictService:
    """系统字典服务类"""
    
    def __init__(self, db: Session):
        """初始化系统字典服务"""
        self.db = db
        self.system_dict_repository = SystemDictRepository(db)
        self.system_dict_item_repository = SystemDictItemRepository(db)
    
    def get_dict_by_id(self, dict_id: int, tenant_id: Optional[int] = None) -> SystemDictModel:
        """根据ID获取字典"""
        dict_obj = self.system_dict_repository.get_by_id(dict_id, tenant_id=tenant_id)
        if not dict_obj:
            raise NotFoundException(detail="字典不存在")
        return dict_obj
    
    def get_dict_with_items(self, dict_id: int, tenant_id: Optional[int] = None) -> SystemDictWithItemsResponse:
        """根据ID获取字典及字典项"""
        dict_obj = self.get_dict_by_id(dict_id, tenant_id)
        items = self.system_dict_item_repository.get_active_items_by_dict_id(dict_id, tenant_id or dict_obj.tenant_id)
        
        return SystemDictWithItemsResponse(
            **SystemDictResponse.model_validate(dict_obj).model_dump(),
            items=[SystemDictItemResponse.model_validate(item) for item in items]
        )
    
    def get_dict_by_code(self, code: str, tenant_id: int) -> SystemDictModel:
        """根据编码获取字典"""
        cache_key = SYSTEM_DICT_BY_CODE.format(dict_code=code, tenant_id=tenant_id)
        cached_data = cache.get_json(cache_key)
        
        if cached_data:
            dict_obj = SystemDictModel(**cached_data)
            return dict_obj
        
        dict_obj = self.system_dict_repository.get_by_code(code, tenant_id)
        if not dict_obj:
            raise NotFoundException(detail="字典不存在")
        
        cache.set_json(cache_key, {
            "id": dict_obj.id,
            "tenant_id": dict_obj.tenant_id,
            "name": dict_obj.name,
            "code": dict_obj.code,
            "description": dict_obj.description,
            "status": dict_obj.status,
            "sort": dict_obj.sort
        }, expire=CACHE_EXPIRE_1_HOUR)
        
        return dict_obj
    
    def get_dict_items_by_code(self, code: str, tenant_id: int) -> List[SystemDictItemResponse]:
        """根据字典编码获取字典项"""
        cache_key = SYSTEM_DICT_ITEMS_BY_CODE.format(dict_code=code, tenant_id=tenant_id)
        cached_data = cache.get_json(cache_key)
        
        if cached_data:
            return [SystemDictItemResponse(**item) for item in cached_data]
        
        items = self.system_dict_item_repository.get_by_dict_code(code, tenant_id)
        result = [SystemDictItemResponse.model_validate(item) for item in items]
        
        cache.set_json(cache_key, [item.model_dump() for item in result], expire=CACHE_EXPIRE_5_MINUTES)
        
        return result
    
    def create_dict(self, dict_create: SystemDictCreate, tenant_id: int) -> SystemDictModel:
        """创建字典"""
        existing_dict = self.system_dict_repository.get_by_code(dict_create.code, tenant_id)
        if existing_dict:
            raise ValidationException(detail="字典编码已存在")
        
        dict_obj = SystemDictModel(
            tenant_id=tenant_id,
            name=dict_create.name,
            code=dict_create.code,
            description=dict_create.description,
            sort=dict_create.sort or 0,
            status=dict_create.status or 1
        )
        
        result = self.system_dict_repository.create(dict_obj)
        
        cache.delete_pattern(f"rbac:dict:*:{tenant_id}")
        
        return result
    
    def update_dict(self, dict_id: int, dict_update: SystemDictUpdate, tenant_id: Optional[int] = None) -> SystemDictModel:
        """更新字典"""
        dict_obj = self.get_dict_by_id(dict_id, tenant_id)
        
        if dict_update.code and dict_update.code != dict_obj.code:
            existing_dict = self.system_dict_repository.get_by_code(dict_update.code, tenant_id or dict_obj.tenant_id)
            if existing_dict:
                raise ValidationException(detail="字典编码已存在")
        
        update_data = dict_update.model_dump(exclude_unset=True)
        result = self.system_dict_repository.update(dict_obj, update_data)
        
        actual_tenant_id = tenant_id or dict_obj.tenant_id
        cache.delete_pattern(f"rbac:dict:*:{actual_tenant_id}")
        
        return result
    
    def delete_dict(self, dict_id: int, tenant_id: Optional[int] = None):
        """删除字典（软删除）"""
        dict_obj = self.get_dict_by_id(dict_id, tenant_id)
        
        self.system_dict_item_repository.delete_by_dict_id(dict_id, tenant_id or dict_obj.tenant_id)
        self.system_dict_repository.delete(dict_obj)
        
        actual_tenant_id = tenant_id or dict_obj.tenant_id
        cache.delete_pattern(f"rbac:dict:*:{actual_tenant_id}")
    
    def paginate_dicts(
        self,
        tenant_id: int,
        keyword: str = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[SystemDictModel]]:
        """分页查询字典"""
        return self.system_dict_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            status=status,
            page=page,
            page_size=page_size
        )
    
    def get_all_active_dicts(self, tenant_id: int) -> List[SystemDictModel]:
        """获取所有活跃字典"""
        return self.system_dict_repository.get_active_dicts(tenant_id)
    
    def get_dict_item_by_id(self, item_id: int, tenant_id: Optional[int] = None) -> SystemDictItemModel:
        """根据ID获取字典项"""
        item = self.system_dict_item_repository.get_by_id(item_id, tenant_id=tenant_id)
        if not item:
            raise NotFoundException(detail="字典项不存在")
        return item
    
    def create_dict_item(self, dict_id: int, item_create: SystemDictItemCreate, tenant_id: int) -> SystemDictItemModel:
        """创建字典项"""
        dict_obj = self.get_dict_by_id(dict_id, tenant_id)
        
        existing_item = self.system_dict_item_repository.get_by_value(dict_id, item_create.value, tenant_id)
        if existing_item:
            raise ValidationException(detail="字典项值已存在")
        
        item = SystemDictItemModel(
            tenant_id=tenant_id,
            dict_id=dict_id,
            label=item_create.label,
            value=item_create.value,
            sort=item_create.sort or 0,
            description=item_create.description,
            status=item_create.status or 1
        )
        
        result = self.system_dict_item_repository.create(item)
        
        cache.delete_pattern(f"rbac:dict:items:*:{tenant_id}")
        
        return result
    
    def update_dict_item(self, item_id: int, item_update: SystemDictItemUpdate, tenant_id: Optional[int] = None) -> SystemDictItemModel:
        """更新字典项"""
        item = self.get_dict_item_by_id(item_id, tenant_id)
        
        if item_update.value and item_update.value != item.value:
            existing_item = self.system_dict_item_repository.get_by_value(item.dict_id, item_update.value, tenant_id or item.tenant_id)
            if existing_item:
                raise ValidationException(detail="字典项值已存在")
        
        update_data = item_update.model_dump(exclude_unset=True)
        result = self.system_dict_item_repository.update(item, update_data)
        
        actual_tenant_id = tenant_id or item.tenant_id
        cache.delete_pattern(f"rbac:dict:items:*:{actual_tenant_id}")
        
        return result
    
    def delete_dict_item(self, item_id: int, tenant_id: Optional[int] = None):
        """删除字典项（软删除）"""
        item = self.get_dict_item_by_id(item_id, tenant_id)
        self.system_dict_item_repository.delete(item)
        
        actual_tenant_id = tenant_id or item.tenant_id
        cache.delete_pattern(f"rbac:dict:items:*:{actual_tenant_id}")
    
    def get_dict_items_by_dict_id(self, dict_id: int, tenant_id: int) -> List[SystemDictItemModel]:
        """根据字典ID获取字典项"""
        return self.system_dict_item_repository.get_by_dict_id(dict_id, tenant_id)
