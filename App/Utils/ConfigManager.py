"""Config Manager"""

import json
from typing import Any, Optional
from sqlalchemy.orm import Session
from App.Services.SystemConfigService import SystemConfigService
from App.Config.Settings import settings


class ConfigManager:
    """配置管理类"""

    @staticmethod
    def get_str(db: Session, key: str, tenant_id: int, default: Optional[str] = None) -> Optional[str]:
        """获取字符串配置"""
        config_service = SystemConfigService(db)
        value = config_service.get_config_value(key, tenant_id)
        if value is not None:
            return value
        return getattr(settings, key, default)

    @staticmethod
    def get_int(db: Session, key: str, tenant_id: int, default: Optional[int] = None) -> Optional[int]:
        """获取整数配置"""
        config_service = SystemConfigService(db)
        value = config_service.get_config_value(key, tenant_id)
        if value is not None:
            try:
                return int(value)
            except (ValueError, TypeError):
                pass
        return getattr(settings, key, default)

    @staticmethod
    def get_bool(db: Session, key: str, tenant_id: int, default: Optional[bool] = None) -> Optional[bool]:
        """获取布尔配置"""
        config_service = SystemConfigService(db)
        value = config_service.get_config_value(key, tenant_id)
        if value is not None:
            try:
                if isinstance(value, str):
                    return value.lower() in ('true', '1', 'yes', 'on')
                return bool(value)
            except (ValueError, TypeError):
                pass
        return getattr(settings, key, default)

    @staticmethod
    def get_json(db: Session, key: str, tenant_id: int, default: Optional[Any] = None) -> Optional[Any]:
        """获取JSON配置"""
        config_service = SystemConfigService(db)
        value = config_service.get_config_value(key, tenant_id)
        if value is not None:
            try:
                return json.loads(value)
            except (ValueError, TypeError, json.JSONDecodeError):
                pass
        return getattr(settings, key, default)

    @staticmethod
    def get_list(db: Session, key: str, tenant_id: int, separator: str = ',', default: Optional[list] = None) -> Optional[list]:
        """获取列表配置（逗号分隔字符串）"""
        config_service = SystemConfigService(db)
        value = config_service.get_config_value(key, tenant_id)
        if value is not None:
            try:
                if isinstance(value, str):
                    return [item.strip() for item in value.split(separator) if item.strip()]
                return value
            except (ValueError, TypeError):
                pass
        settings_value = getattr(settings, key, default)
        if isinstance(settings_value, str):
            return [item.strip() for item in settings_value.split(separator) if item.strip()]
        return settings_value
