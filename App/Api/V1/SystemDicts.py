"""System Dictionary Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from App.Schemas.SystemDict import (
    SystemDictCreate,
    SystemDictUpdate,
    SystemDictItemCreate,
    SystemDictItemUpdate
)
from App.Schemas.Auth import AuthResponse
from App.Services.SystemDictService import SystemDictService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/system-dicts",
    tags=["系统字典管理"]
)


@router.get("", response_model=AuthResponse, summary="获取字典列表", dependencies=[Depends(permission_dependency("dict:view"))])
def get_dicts(
    keyword: str = None,
    status: int = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取字典列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        
        total, dicts = dict_service.paginate_dicts(
            tenant_id=tenant_id,
            keyword=keyword,
            status=status,
            page=page,
            page_size=page_size
        )
        
        dict_list = []
        for d in dicts:
            dict_list.append({
                "id": d.id,
                "name": d.name,
                "code": d.code,
                "description": d.description,
                "sort": d.sort,
                "status": d.status,
                "create_time": d.create_time.isoformat() if hasattr(d.create_time, 'isoformat') else d.create_time,
                "update_time": d.update_time.isoformat() if hasattr(d.update_time, 'isoformat') else d.update_time
            })
        
        return ResponseUtils.pagination(
            data=dict_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取字典列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_dicts: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/active", response_model=AuthResponse, summary="获取活跃字典列表")
def get_active_dicts(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取活跃字典列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        dicts = dict_service.get_all_active_dicts(tenant_id)
        
        dict_list = []
        for d in dicts:
            dict_list.append({
                "id": d.id,
                "name": d.name,
                "code": d.code
            })
        
        return ResponseUtils.success(data=dict_list, message="获取活跃字典列表成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_active_dicts: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{dict_id}", response_model=AuthResponse, summary="获取字典详情", dependencies=[Depends(permission_dependency("dict:view"))])
def get_dict(
    dict_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取字典详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        dict_with_items = dict_service.get_dict_with_items(dict_id, tenant_id=tenant_id)
        
        return ResponseUtils.success(data=dict_with_items.model_dump(), message="获取字典详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_dict: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/code/{code}", response_model=AuthResponse, summary="根据编码获取字典项")
def get_dict_items_by_code(
    code: str,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """根据编码获取字典项接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        items = dict_service.get_dict_items_by_code(code, tenant_id)
        
        item_list = []
        for item in items:
            item_list.append({
                "label": item.label,
                "value": item.value,
                "sort": item.sort
            })
        
        return ResponseUtils.success(data=item_list, message="获取字典项成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_dict_items_by_code: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("", response_model=AuthResponse, summary="创建字典", dependencies=[Depends(permission_dependency("dict:create"))])
def create_dict(
    dict_data: SystemDictCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建字典接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        dict_obj = dict_service.create_dict(dict_data, tenant_id=tenant_id)
        
        dict_info = {
            "id": dict_obj.id,
            "name": dict_obj.name,
            "code": dict_obj.code,
            "description": dict_obj.description,
            "sort": dict_obj.sort,
            "status": dict_obj.status
        }
        
        return ResponseUtils.success(data=dict_info, message="创建字典成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in create_dict: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{dict_id}", response_model=AuthResponse, summary="更新字典", dependencies=[Depends(permission_dependency("dict:update"))])
def update_dict(
    dict_id: int,
    dict_data: SystemDictUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新字典接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        dict_obj = dict_service.update_dict(dict_id, dict_data, tenant_id=tenant_id)
        
        dict_info = {
            "id": dict_obj.id,
            "name": dict_obj.name,
            "code": dict_obj.code,
            "description": dict_obj.description,
            "sort": dict_obj.sort,
            "status": dict_obj.status
        }
        
        return ResponseUtils.success(data=dict_info, message="更新字典成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in update_dict: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/{dict_id}", response_model=AuthResponse, summary="删除字典", dependencies=[Depends(permission_dependency("dict:delete"))])
def delete_dict(
    dict_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除字典接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        dict_service.delete_dict(dict_id, tenant_id=tenant_id)
        
        return ResponseUtils.success(message="删除字典成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in delete_dict: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("/{dict_id}/items", response_model=AuthResponse, summary="创建字典项", dependencies=[Depends(permission_dependency("dict:create"))])
def create_dict_item(
    dict_id: int,
    item_data: SystemDictItemCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建字典项接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        item = dict_service.create_dict_item(dict_id, item_data, tenant_id=tenant_id)
        
        item_info = {
            "id": item.id,
            "dict_id": item.dict_id,
            "label": item.label,
            "value": item.value,
            "sort": item.sort,
            "description": item.description,
            "status": item.status
        }
        
        return ResponseUtils.success(data=item_info, message="创建字典项成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in create_dict_item: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/items/{item_id}", response_model=AuthResponse, summary="更新字典项", dependencies=[Depends(permission_dependency("dict:update"))])
def update_dict_item(
    item_id: int,
    item_data: SystemDictItemUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新字典项接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        item = dict_service.update_dict_item(item_id, item_data, tenant_id=tenant_id)
        
        item_info = {
            "id": item.id,
            "dict_id": item.dict_id,
            "label": item.label,
            "value": item.value,
            "sort": item.sort,
            "description": item.description,
            "status": item.status
        }
        
        return ResponseUtils.success(data=item_info, message="更新字典项成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in update_dict_item: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/items/{item_id}", response_model=AuthResponse, summary="删除字典项", dependencies=[Depends(permission_dependency("dict:delete"))])
def delete_dict_item(
    item_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除字典项接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        dict_service.delete_dict_item(item_id, tenant_id=tenant_id)
        
        return ResponseUtils.success(message="删除字典项成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in delete_dict_item: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{dict_id}/items", response_model=AuthResponse, summary="获取字典项列表", dependencies=[Depends(permission_dependency("dict:view"))])
def get_dict_items(
    dict_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取字典项列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        dict_service = SystemDictService(db)
        items = dict_service.get_dict_items_by_dict_id(dict_id, tenant_id=tenant_id)
        
        item_list = []
        for item in items:
            item_list.append({
                "id": item.id,
                "dict_id": item.dict_id,
                "label": item.label,
                "value": item.value,
                "sort": item.sort,
                "description": item.description,
                "status": item.status,
                "create_time": item.create_time.isoformat() if hasattr(item.create_time, 'isoformat') else item.create_time,
                "update_time": item.update_time.isoformat() if hasattr(item.update_time, 'isoformat') else item.update_time
            })
        
        return ResponseUtils.success(data=item_list, message="获取字典项列表成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_dict_items: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
