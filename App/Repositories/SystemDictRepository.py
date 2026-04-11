"""System Dict Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from App.Models.SystemDict import SystemDictModel
from App.Models.SystemDictItem import SystemDictItemModel
from App.Repositories.Base import BaseRepository


class SystemDictRepository(BaseRepository[SystemDictModel]):
    """系统字典仓储类"""
    
    def __init__(self, db: Session):
        """初始化系统字典仓储"""
        super().__init__(db, SystemDictModel)
    
    def get_by_code(self, code: str, tenant_id: int) -> Optional[SystemDictModel]:
        """根据字典编码获取字典"""
        return self.db.query(SystemDictModel).filter(
            SystemDictModel.code == code,
            SystemDictModel.tenant_id == tenant_id,
            SystemDictModel.is_deleted == 0
        ).first()
    
    def get_by_name(self, name: str, tenant_id: int) -> Optional[SystemDictModel]:
        """根据字典名称获取字典"""
        return self.db.query(SystemDictModel).filter(
            SystemDictModel.name == name,
            SystemDictModel.tenant_id == tenant_id,
            SystemDictModel.is_deleted == 0
        ).first()
    
    def get_active_dicts(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[SystemDictModel]:
        """获取活跃字典"""
        return self.db.query(SystemDictModel).filter(
            SystemDictModel.tenant_id == tenant_id,
            SystemDictModel.is_deleted == 0,
            SystemDictModel.status == 1
        ).order_by(SystemDictModel.sort, SystemDictModel.create_time.desc()).offset(skip).limit(limit).all()
    
    def search(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[SystemDictModel]:
        """搜索字典"""
        return self.db.query(SystemDictModel).filter(
            or_(
                SystemDictModel.name.like(f"%{keyword}%"),
                SystemDictModel.code.like(f"%{keyword}%"),
                SystemDictModel.description.like(f"%{keyword}%")
            ),
            SystemDictModel.tenant_id == tenant_id,
            SystemDictModel.is_deleted == 0,
            SystemDictModel.status == 1
        ).order_by(SystemDictModel.sort, SystemDictModel.create_time.desc()).offset(skip).limit(limit).all()
    
    def paginate(
        self,
        tenant_id: int,
        keyword: str = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[SystemDictModel]]:
        """分页查询字典"""
        query = self.db.query(SystemDictModel).filter(
            SystemDictModel.tenant_id == tenant_id,
            SystemDictModel.is_deleted == 0
        )
        
        if keyword:
            query = query.filter(
                or_(
                    SystemDictModel.name.like(f"%{keyword}%"),
                    SystemDictModel.code.like(f"%{keyword}%")
                )
            )
        
        if status is not None:
            query = query.filter(SystemDictModel.status == status)
        
        total = query.count()
        items = query.order_by(SystemDictModel.sort, SystemDictModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()
        
        return total, items


class SystemDictItemRepository(BaseRepository[SystemDictItemModel]):
    """系统字典项仓储类"""
    
    def __init__(self, db: Session):
        """初始化系统字典项仓储"""
        super().__init__(db, SystemDictItemModel)
    
    def get_by_dict_id(self, dict_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[SystemDictItemModel]:
        """根据字典ID获取字典项"""
        return self.db.query(SystemDictItemModel).filter(
            SystemDictItemModel.dict_id == dict_id,
            SystemDictItemModel.tenant_id == tenant_id,
            SystemDictItemModel.is_deleted == 0
        ).order_by(SystemDictItemModel.sort, SystemDictItemModel.create_time.desc()).offset(skip).limit(limit).all()
    
    def get_active_items_by_dict_id(self, dict_id: int, tenant_id: int) -> List[SystemDictItemModel]:
        """根据字典ID获取活跃字典项"""
        return self.db.query(SystemDictItemModel).filter(
            SystemDictItemModel.dict_id == dict_id,
            SystemDictItemModel.tenant_id == tenant_id,
            SystemDictItemModel.is_deleted == 0,
            SystemDictItemModel.status == 1
        ).order_by(SystemDictItemModel.sort, SystemDictItemModel.create_time.desc()).all()
    
    def get_by_dict_code(self, dict_code: str, tenant_id: int) -> List[SystemDictItemModel]:
        """根据字典编码获取字典项"""
        dict_obj = self.db.query(SystemDictModel).filter(
            SystemDictModel.code == dict_code,
            SystemDictModel.tenant_id == tenant_id,
            SystemDictModel.is_deleted == 0,
            SystemDictModel.status == 1
        ).first()
        
        if not dict_obj:
            return []
        
        return self.db.query(SystemDictItemModel).filter(
            SystemDictItemModel.dict_id == dict_obj.id,
            SystemDictItemModel.tenant_id == tenant_id,
            SystemDictItemModel.is_deleted == 0,
            SystemDictItemModel.status == 1
        ).order_by(SystemDictItemModel.sort, SystemDictItemModel.create_time.desc()).all()
    
    def get_by_value(self, dict_id: int, value: str, tenant_id: int) -> Optional[SystemDictItemModel]:
        """根据值获取字典项"""
        return self.db.query(SystemDictItemModel).filter(
            SystemDictItemModel.dict_id == dict_id,
            SystemDictItemModel.value == value,
            SystemDictItemModel.tenant_id == tenant_id,
            SystemDictItemModel.is_deleted == 0
        ).first()
    
    def delete_by_dict_id(self, dict_id: int, tenant_id: int):
        """根据字典ID删除字典项（软删除）"""
        self.db.query(SystemDictItemModel).filter(
            SystemDictItemModel.dict_id == dict_id,
            SystemDictItemModel.tenant_id == tenant_id,
            SystemDictItemModel.is_deleted == 0
        ).update({
            SystemDictItemModel.is_deleted: 1,
            SystemDictItemModel.update_time: SystemDictItemModel.update_time
        }, synchronize_session=False)
    
    def paginate(
        self,
        tenant_id: int,
        dict_id: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[SystemDictItemModel]]:
        """分页查询字典项"""
        query = self.db.query(SystemDictItemModel).filter(
            SystemDictItemModel.tenant_id == tenant_id,
            SystemDictItemModel.is_deleted == 0
        )
        
        if dict_id is not None:
            query = query.filter(SystemDictItemModel.dict_id == dict_id)
        
        if status is not None:
            query = query.filter(SystemDictItemModel.status == status)
        
        total = query.count()
        items = query.order_by(SystemDictItemModel.sort, SystemDictItemModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()
        
        return total, items
