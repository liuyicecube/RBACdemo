"""System Config Service"""

from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from App.Models.SystemConfig import SystemConfigModel
from App.Repositories.SystemConfigRepository import SystemConfigRepository
from App.Schemas.SystemConfig import (
    SystemConfigCreate,
    SystemConfigUpdate,
    SystemConfigResponse
)
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Utils.Cache import cache
from App.Config.CacheKeys import (
    SYSTEM_CONFIG_ALL,
    SYSTEM_CONFIG_BY_KEY,
    CACHE_EXPIRE_12_HOURS
)


class SystemConfigService:
    """系统配置服务类"""

    def __init__(self, db: Session):
        """初始化系统配置服务"""
        self.db = db
        self.system_config_repository = SystemConfigRepository(db)
        self._config_cache: Dict[int, Dict[str, str]] = {}

    def get_config_by_id(self, config_id: int, tenant_id: Optional[int] = None) -> SystemConfigModel:
        """根据ID获取配置"""
        config = self.system_config_repository.get_by_id(config_id, tenant_id=tenant_id)
        if not config:
            raise NotFoundException(detail="配置不存在")
        return config

    def get_config_by_key(self, key: str, tenant_id: int) -> SystemConfigModel:
        """根据键获取配置"""
        config = self.system_config_repository.get_by_key(key, tenant_id)
        if not config:
            raise NotFoundException(detail="配置不存在")
        return config

    def get_config_value(self, key: str, tenant_id: int, default: str = None) -> Optional[str]:
        """获取配置值"""
        cache_key = SYSTEM_CONFIG_BY_KEY.format(config_key=key, tenant_id=tenant_id)
        cached_value = cache.get(cache_key)

        if cached_value is not None:
            return cached_value

        if tenant_id in self._config_cache and key in self._config_cache[tenant_id]:
            return self._config_cache[tenant_id][key]

        try:
            config = self.get_config_by_key(key, tenant_id)
            if config.status == 1:
                if tenant_id not in self._config_cache:
                    self._config_cache[tenant_id] = {}
                self._config_cache[tenant_id][key] = config.config_value
                cache.set(cache_key, config.config_value, expire=CACHE_EXPIRE_12_HOURS)
                return config.config_value
        except NotFoundException:
            pass

        return default

    def create_config(self, config_create: SystemConfigCreate, tenant_id: int) -> SystemConfigModel:
        """创建配置"""
        existing_config = self.system_config_repository.get_by_key(config_create.config_key, tenant_id)
        if existing_config:
            raise ValidationException(detail="配置键已存在")

        config = SystemConfigModel(
            tenant_id=tenant_id,
            config_key=config_create.config_key,
            config_value=config_create.config_value,
            group_name=config_create.group_name,
            description=config_create.description,
            config_type=config_create.config_type or "string",
            is_system=config_create.is_system or 0,
            sort=config_create.sort or 0,
            status=config_create.status or 1
        )

        result = self.system_config_repository.create(config)
        self._clear_cache(tenant_id)
        return result

    def update_config(self, config_id: int, config_update: SystemConfigUpdate, tenant_id: Optional[int] = None) -> SystemConfigModel:
        """更新配置"""
        config = self.get_config_by_id(config_id, tenant_id)

        update_data = config_update.model_dump(exclude_unset=True)
        result = self.system_config_repository.update(config, update_data)
        self._clear_cache(tenant_id or result.tenant_id)
        return result

    def delete_config(self, config_id: int, tenant_id: Optional[int] = None):
        """删除配置（软删除）"""
        config = self.get_config_by_id(config_id, tenant_id)
        self.system_config_repository.delete(config)
        self._clear_cache(tenant_id or config.tenant_id)

    def paginate_configs(
        self,
        tenant_id: int,
        keyword: str = None,
        group_name: str = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[SystemConfigModel]]:
        """分页查询配置"""
        return self.system_config_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            group_name=group_name,
            status=status,
            page=page,
            page_size=page_size
        )

    def get_all_active_configs(self, tenant_id: int) -> List[SystemConfigModel]:
        """获取所有活跃配置"""
        return self.system_config_repository.get_active_configs(tenant_id)

    def get_configs_by_group(self, group: str, tenant_id: int) -> List[SystemConfigModel]:
        """根据分组获取配置"""
        return self.system_config_repository.get_by_group(group, tenant_id)

    def get_config_groups(self, tenant_id: int) -> List[str]:
        """获取所有配置分组"""
        return self.system_config_repository.get_groups(tenant_id)

    def get_configs_grouped(self, tenant_id: int) -> Dict[str, List[SystemConfigModel]]:
        """获取所有配置并按分组整理"""
        return self.system_config_repository.get_by_group_dict(tenant_id)

    def batch_update_configs(self, configs_data: Dict[str, str], tenant_id: int) -> List[SystemConfigModel]:
        """批量更新配置"""
        updated_configs = []
        for key, value in configs_data.items():
            try:
                config = self.get_config_by_key(key, tenant_id)
                updated_config = self.system_config_repository.update(config, {"config_value": value})
                updated_configs.append(updated_config)
            except NotFoundException:
                continue

        self._clear_cache(tenant_id)
        return updated_configs

    def refresh_cache(self, tenant_id: int):
        """刷新配置缓存"""
        self._clear_cache(tenant_id)
        configs = self.get_all_active_configs(tenant_id)
        self._config_cache[tenant_id] = {config.config_key: config.config_value for config in configs}

    def _clear_cache(self, tenant_id: int):
        """清除指定租户的缓存"""
        if tenant_id in self._config_cache:
            del self._config_cache[tenant_id]
        cache.delete_pattern(f"rbac:config:*:{tenant_id}")
