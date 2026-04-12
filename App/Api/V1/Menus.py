"""Menu Management API"""

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from App.Schemas.Menu import (
    MenuCreate,
    MenuUpdate
)
from App.Schemas.Auth import AuthResponse
from App.Services.MenuService import MenuService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/menus",
    tags=["菜单管理"]
)


@router.get("", response_model=AuthResponse, summary="获取菜单列表", dependencies=[Depends(permission_dependency("menu:view"))])
def get_menus(
    keyword: str = None,
    type: int = None,
    status: int = None,
    parent_id: int = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取菜单列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        menu_service = MenuService(db)

        total, menus = menu_service.paginate_menus(
            tenant_id=tenant_id,
            keyword=keyword,
            menu_type=type,
            status=status,
            page=page,
            page_size=page_size
        )

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
                "create_time": menu.create_time.isoformat() if hasattr(menu.create_time, 'isoformat') else menu.create_time,
                "update_time": menu.update_time.isoformat() if hasattr(menu.update_time, 'isoformat') else menu.update_time
            })

        return ResponseUtils.pagination(
            data=menu_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取菜单列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_menus: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/tree", response_model=AuthResponse, summary="获取菜单树形结构", dependencies=[Depends(permission_dependency("menu:view"))])
def get_menu_tree(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取菜单树形结构接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        menu_service = MenuService(db)
        tree = menu_service.get_menu_tree(tenant_id=tenant_id)

        return ResponseUtils.success(data=tree, message="获取菜单树形结构成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_menu_tree: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/user", response_model=AuthResponse, summary="获取当前用户菜单树")
@router.get("/my", response_model=AuthResponse, summary="获取当前用户菜单树")
def get_user_menu_tree(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取当前用户菜单树接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        menu_service = MenuService(db)
        tree = menu_service.get_user_menu_tree(current_user.id, tenant_id=tenant_id)

        return ResponseUtils.success(data=tree, message="获取用户菜单树成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_user_menu_tree: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/sort", response_model=AuthResponse, summary="菜单排序", dependencies=[Depends(permission_dependency("menu:update"))])
def sort_menus(
    request: Dict[str, List[int]] = Body(...),
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """菜单排序接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        menu_service = MenuService(db)
        menu_service.sort_menus(request.get("menu_ids", []), tenant_id=tenant_id)

        return ResponseUtils.success(message="菜单排序成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in sort_menus: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{menu_id}", response_model=AuthResponse, summary="获取菜单详情", dependencies=[Depends(permission_dependency("menu:view"))])
def get_menu(
    menu_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取菜单详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        menu_service = MenuService(db)
        menu = menu_service.get_menu_by_id(menu_id, tenant_id=tenant_id)

        menu_info = {
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
            "create_time": menu.create_time.isoformat() if hasattr(menu.create_time, 'isoformat') else menu.create_time,
            "update_time": menu.update_time.isoformat() if hasattr(menu.update_time, 'isoformat') else menu.update_time
        }

        return ResponseUtils.success(data=menu_info, message="获取菜单详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_menu: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("", response_model=AuthResponse, summary="创建菜单", dependencies=[Depends(permission_dependency("menu:create"))])
def create_menu(
    menu_data: MenuCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建菜单接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        menu_service = MenuService(db)
        menu = menu_service.create_menu(menu_data.model_dump(), tenant_id=tenant_id, created_by=current_user.id)

        menu_info = {
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
            "status": menu.status
        }

        return ResponseUtils.success(data=menu_info, message="创建菜单成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in create_menu: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{menu_id}", response_model=AuthResponse, summary="更新菜单信息", dependencies=[Depends(permission_dependency("menu:update"))])
def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新菜单信息接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        menu_service = MenuService(db)
        menu = menu_service.update_menu(menu_id, menu_data.model_dump(), tenant_id=tenant_id, updated_by=current_user.id)

        menu_info = {
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
            "status": menu.status
        }

        return ResponseUtils.success(data=menu_info, message="更新菜单信息成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in update_menu: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/{menu_id}", response_model=AuthResponse, summary="删除菜单", dependencies=[Depends(permission_dependency("menu:delete"))])
def delete_menu(
    menu_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除菜单接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        menu_service = MenuService(db)
        menu_service.delete_menu(menu_id, tenant_id=tenant_id)

        return ResponseUtils.success(message="删除菜单成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in delete_menu: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{menu_id}/status", response_model=AuthResponse, summary="更新菜单状态", dependencies=[Depends(permission_dependency("menu:update"))])
def update_menu_status(
    menu_id: int,
    status: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新菜单状态接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        menu_service = MenuService(db)
        menu = menu_service.update_menu_status(menu_id, status, tenant_id=tenant_id, updated_by=current_user.id)

        menu_info = {
            "id": menu.id,
            "name": menu.name,
            "status": menu.status
        }

        return ResponseUtils.success(data=menu_info, message="更新菜单状态成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in update_menu_status: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{menu_id}/children", response_model=AuthResponse, summary="获取菜单的子菜单列表", dependencies=[Depends(permission_dependency("menu:view"))])
def get_menu_children(
    menu_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取菜单的子菜单列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        menu_service = MenuService(db)
        children_menus = menu_service.get_menu_children(menu_id, tenant_id=tenant_id)

        children_list = []
        for menu in children_menus:
            children_list.append({
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
                "status": menu.status
            })

        return ResponseUtils.success(
            data={
                "menu_id": menu_id,
                "children": children_list
            },
            message="获取子菜单列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_menu_children: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
