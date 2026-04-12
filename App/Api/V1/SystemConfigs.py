"""System Config Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from App.Schemas.SystemConfig import (
    SystemConfigCreate,
    SystemConfigUpdate
)
from App.Schemas.Auth import AuthResponse
from App.Services.SystemConfigService import SystemConfigService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/system-configs",
    tags=["系统配置管理"]
)


@router.get("", response_model=AuthResponse, summary="获取配置列表", dependencies=[Depends(permission_dependency("config:view"))])
def get_configs(
    keyword: str = None,
    group_name: str = None,
    status: int = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取配置列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)

        total, configs = config_service.paginate_configs(
            tenant_id=tenant_id,
            keyword=keyword,
            group_name=group_name,
            status=status,
            page=page,
            page_size=page_size
        )

        config_list = []
        for config in configs:
            config_list.append({
                "id": config.id,
                "config_key": config.config_key,
                "config_value": config.config_value,
                "config_type": config.config_type,
                "group_name": config.group_name,
                "is_system": config.is_system,
                "description": config.description,
                "sort": config.sort,
                "status": config.status,
                "create_time": config.create_time.isoformat() if hasattr(config.create_time, 'isoformat') else config.create_time,
                "update_time": config.update_time.isoformat() if hasattr(config.update_time, 'isoformat') else config.update_time
            })

        return ResponseUtils.pagination(
            data=config_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取配置列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_configs: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/groups", response_model=AuthResponse, summary="获取配置分组列表")
def get_config_groups(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取配置分组列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)
        groups = config_service.get_config_groups(tenant_id)

        return ResponseUtils.success(data=groups, message="获取配置分组列表成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_config_groups: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/grouped", response_model=AuthResponse, summary="获取分组配置")
def get_grouped_configs(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取分组配置接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)
        grouped_configs = config_service.get_configs_grouped(tenant_id)

        result = {}
        for group, configs in grouped_configs.items():
            result[group] = []
            for config in configs:
                result[group].append({
                    "config_key": config.config_key,
                    "config_value": config.config_value,
                    "config_type": config.config_type
                })

        return ResponseUtils.success(data=result, message="获取分组配置成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_grouped_configs: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/active", response_model=AuthResponse, summary="获取活跃配置")
def get_active_configs(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取活跃配置接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)
        configs = config_service.get_all_active_configs(tenant_id)

        config_dict = {}
        for config in configs:
            config_dict[config.config_key] = config.config_value

        return ResponseUtils.success(data=config_dict, message="获取活跃配置成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_active_configs: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{config_id}", response_model=AuthResponse, summary="获取配置详情", dependencies=[Depends(permission_dependency("config:view"))])
def get_config(
    config_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取配置详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)
        config = config_service.get_config_by_id(config_id, tenant_id=tenant_id)

        config_info = {
            "id": config.id,
            "config_key": config.config_key,
            "config_value": config.config_value,
            "config_type": config.config_type,
            "group_name": config.group_name,
            "is_system": config.is_system,
            "description": config.description,
            "sort": config.sort,
            "status": config.status,
            "create_time": config.create_time.isoformat() if hasattr(config.create_time, 'isoformat') else config.create_time,
            "update_time": config.update_time.isoformat() if hasattr(config.update_time, 'isoformat') else config.update_time
        }

        return ResponseUtils.success(data=config_info, message="获取配置详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_config: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/key/{key}", response_model=AuthResponse, summary="根据键获取配置值")
def get_config_value(
    key: str,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """根据键获取配置值接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)
        value = config_service.get_config_value(key, tenant_id)

        return ResponseUtils.success(data={"key": key, "value": value}, message="获取配置值成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_config_value: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("", response_model=AuthResponse, summary="创建配置", dependencies=[Depends(permission_dependency("config:create"))])
def create_config(
    config_data: SystemConfigCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建配置接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)
        config = config_service.create_config(config_data, tenant_id=tenant_id)

        config_info = {
            "id": config.id,
            "config_key": config.config_key,
            "config_value": config.config_value,
            "config_type": config.config_type,
            "group_name": config.group_name,
            "is_system": config.is_system,
            "description": config.description,
            "sort": config.sort,
            "status": config.status
        }

        return ResponseUtils.success(data=config_info, message="创建配置成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in create_config: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{config_id}", response_model=AuthResponse, summary="更新配置", dependencies=[Depends(permission_dependency("config:update"))])
def update_config(
    config_id: int,
    config_data: SystemConfigUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新配置接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)
        config = config_service.update_config(config_id, config_data, tenant_id=tenant_id)

        config_info = {
            "id": config.id,
            "config_key": config.config_key,
            "config_value": config.config_value,
            "config_type": config.config_type,
            "group_name": config.group_name,
            "is_system": config.is_system,
            "description": config.description,
            "sort": config.sort,
            "status": config.status
        }

        return ResponseUtils.success(data=config_info, message="更新配置成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in update_config: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/{config_id}", response_model=AuthResponse, summary="删除配置", dependencies=[Depends(permission_dependency("config:delete"))])
def delete_config(
    config_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除配置接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)
        config_service.delete_config(config_id, tenant_id=tenant_id)

        return ResponseUtils.success(message="删除配置成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in delete_config: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/batch", response_model=AuthResponse, summary="批量更新配置", dependencies=[Depends(permission_dependency("config:update"))])
def batch_update_configs(
    configs_data: Dict[str, str],
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """批量更新配置接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)
        updated_configs = config_service.batch_update_configs(configs_data, tenant_id=tenant_id)

        result = []
        for config in updated_configs:
            result.append({
                "id": config.id,
                "config_key": config.config_key,
                "config_value": config.config_value
            })

        return ResponseUtils.success(data=result, message="批量更新配置成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in batch_update_configs: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("/refresh-cache", response_model=AuthResponse, summary="刷新配置缓存", dependencies=[Depends(permission_dependency("config:update"))])
def refresh_config_cache(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """刷新配置缓存接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        config_service = SystemConfigService(db)
        config_service.refresh_cache(tenant_id=tenant_id)

        return ResponseUtils.success(message="刷新配置缓存成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in refresh_config_cache: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
