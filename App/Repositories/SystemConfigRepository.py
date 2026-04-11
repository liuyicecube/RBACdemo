"""System Config Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from App.Models.SystemConfig import SystemConfigModel
from App.Repositories.Base import BaseRepository


class SystemConfigRepository(BaseRepository[SystemConfigModel]):
    """系统配置仓储类"""
    
    def __init__(self, db: Session):
        """初始化系统配置仓储"""
        super().__init__(db, SystemConfigModel)
    
    def get_by_key(self, key: str, tenant_id: int) -> Optional[SystemConfigModel]:
        """根据配置键获取配置"""
        return self.db.query(SystemConfigModel).filter(
            SystemConfigModel.config_key == key,
            SystemConfigModel.tenant_id == tenant_id,
            SystemConfigModel.is_deleted == 0
        ).first()
    
    def get_by_name(self, name: str, tenant_id: int) -> Optional[SystemConfigModel]:
        """根据配置名称获取配置"""
        return self.db.query(SystemConfigModel).filter(
            SystemConfigModel.config_key == name,
            SystemConfigModel.tenant_id == tenant_id,
            SystemConfigModel.is_deleted == 0
        ).first()
    
    def get_by_group(self, group: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[SystemConfigModel]:
        """根据分组获取配置"""
        return self.db.query(SystemConfigModel).filter(
            SystemConfigModel.group_name == group,
            SystemConfigModel.tenant_id == tenant_id,
            SystemConfigModel.is_deleted == 0
        ).order_by(SystemConfigModel.sort, SystemConfigModel.create_time.desc()).offset(skip).limit(limit).all()
    
    def get_active_configs(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[SystemConfigModel]:
        """获取活跃配置"""
        return self.db.query(SystemConfigModel).filter(
            SystemConfigModel.tenant_id == tenant_id,
            SystemConfigModel.is_deleted == 0,
            SystemConfigModel.status == 1
        ).order_by(SystemConfigModel.sort, SystemConfigModel.create_time.desc()).offset(skip).limit(limit).all()
    
    def get_groups(self, tenant_id: int) -> List[str]:
        """获取所有配置分组"""
        result = self.db.query(SystemConfigModel.group_name).filter(
            SystemConfigModel.tenant_id == tenant_id,
            SystemConfigModel.is_deleted == 0,
            SystemConfigModel.group_name.isnot(None)
        ).distinct().all()
        return [item.group_name for item in result if item.group_name]
    
    def get_by_group_dict(self, tenant_id: int) -> dict:
        """获取所有配置并按分组整理"""
        configs = self.get_active_configs(tenant_id)
        group_dict = {}
        for config in configs:
            group = config.group_name or "default"
            if group not in group_dict:
                group_dict[group] = []
            group_dict[group].append(config)
        return group_dict
    
    def search(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[SystemConfigModel]:
        """搜索配置"""
        return self.db.query(SystemConfigModel).filter(
            or_(
                SystemConfigModel.config_key.like(f"%{keyword}%"),
                SystemConfigModel.description.like(f"%{keyword}%")
            ),
            SystemConfigModel.tenant_id == tenant_id,
            SystemConfigModel.is_deleted == 0,
            SystemConfigModel.status == 1
        ).order_by(SystemConfigModel.sort, SystemConfigModel.create_time.desc()).offset(skip).limit(limit).all()
    
    def paginate(
        self,
        tenant_id: int,
        keyword: str = None,
        group_name: str = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[SystemConfigModel]]:
        """分页查询配置"""
        query = self.db.query(SystemConfigModel).filter(
            SystemConfigModel.tenant_id == tenant_id,
            SystemConfigModel.is_deleted == 0
        )
        
        if keyword:
            query = query.filter(
                or_(
                    SystemConfigModel.config_key.like(f"%{keyword}%"),
                    SystemConfigModel.description.like(f"%{keyword}%")
                )
            )
        
        if group_name:
            query = query.filter(SystemConfigModel.group_name == group_name)
        
        if status is not None:
            query = query.filter(SystemConfigModel.status == status)
        
        total = query.count()
        items = query.order_by(SystemConfigModel.sort, SystemConfigModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()
        
        return total, items
