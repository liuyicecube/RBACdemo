"""System Dict Item Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from App.Models.SystemDictItem import SystemDictItemModel
from App.Repositories.Base import BaseRepository


class SystemDictItemRepository(BaseRepository[SystemDictItemModel]):
    """系统字典项仓储类"""

    def __init__(self, db: Session):
        """初始化系统字典项仓储"""
        super().__init__(db, SystemDictItemModel)

    def get_by_dict_id(self, dict_id: int, skip: int = 0, limit: int = 100) -> List[SystemDictItemModel]:
        """根据字典ID获取字典项"""
        return self.db.query(SystemDictItemModel).filter(
            SystemDictItemModel.dict_id == dict_id,
            SystemDictItemModel.status == 1
        ).order_by(SystemDictItemModel.sort).offset(skip).limit(limit).all()

    def get_by_dict_code(self, dict_code: str, skip: int = 0, limit: int = 100) -> List[SystemDictItemModel]:
        """根据字典编码获取字典项"""
        from App.Models.SystemDict import SystemDictModel
        return self.db.query(SystemDictItemModel).join(
            SystemDictModel, SystemDictItemModel.dict_id == SystemDictModel.id
        ).filter(
            SystemDictModel.code == dict_code,
            SystemDictItemModel.status == 1,
            SystemDictModel.status == 1
        ).order_by(SystemDictItemModel.sort).offset(skip).limit(limit).all()

    def get_by_value(self, dict_id: int, value: str) -> Optional[SystemDictItemModel]:
        """根据字典ID和值获取字典项"""
        return self.db.query(SystemDictItemModel).filter(
            SystemDictItemModel.dict_id == dict_id,
            SystemDictItemModel.value == value,
            SystemDictItemModel.status == 1
        ).first()
