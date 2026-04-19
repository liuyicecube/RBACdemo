"""Department Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from App.Schemas.Department import (
    DepartmentCreate,
    DepartmentUpdate
)
from App.Schemas.Auth import AuthResponse
from App.Services.DepartmentService import DepartmentService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/departments",
    tags=["部门管理"]
)


@router.get(
    "",
    response_model=AuthResponse,
    summary="获取部门列表",
    dependencies=[Depends(permission_dependency("department:view"))]
)
def get_departments(
    keyword: str = None,
    status: int = None,
    parent_id: int = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取部门列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        department_service = DepartmentService(db)

        total, departments = department_service.paginate_departments(
            tenant_id=tenant_id,
            keyword=keyword,
            status=status,
            page=page,
            page_size=page_size
        )

        department_list = []
        for dept in departments:
            department_list.append({
                "id": dept.id,
                "name": dept.name,
                "code": dept.code,
                "parent_id": dept.parent_id,
                "level": dept.level,
                "description": dept.description,
                "status": dept.status,
                "create_time": dept.create_time.isoformat() if hasattr(dept.create_time, 'isoformat') else dept.create_time,
                "update_time": dept.update_time.isoformat() if hasattr(dept.update_time, 'isoformat') else dept.update_time
            })

        return ResponseUtils.pagination(
            data=department_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取部门列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback

        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/tree",
    response_model=AuthResponse,
    summary="获取部门树形结构",
    dependencies=[Depends(permission_dependency("department:view"))]
)
def get_department_tree(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取部门树形结构接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        department_service = DepartmentService(db)
        tree = department_service.get_department_tree(tenant_id=tenant_id)

        return ResponseUtils.success(data=tree, message="获取部门树形结构成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback

        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/{department_id}",
    response_model=AuthResponse,
    summary="获取部门详情",
    dependencies=[Depends(permission_dependency("department:view"))]
)
def get_department(
    department_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取部门详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        department_service = DepartmentService(db)
        department = department_service.get_department_by_id(department_id, tenant_id=tenant_id)

        department_info = {
            "id": department.id,
            "name": department.name,
            "code": department.code,
            "parent_id": department.parent_id,
            "level": department.level,
            "description": department.description,
            "status": department.status,
            "create_time": department.create_time.isoformat() if hasattr(department.create_time, 'isoformat') else department.create_time,
            "update_time": department.update_time.isoformat() if hasattr(department.update_time, 'isoformat') else department.update_time
        }

        return ResponseUtils.success(data=department_info, message="获取部门详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback

        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post(
    "",
    response_model=AuthResponse,
    summary="创建部门",
    dependencies=[Depends(permission_dependency("department:create"))]
)
def create_department(
    department_data: DepartmentCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建部门接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        department_service = DepartmentService(db)
        department = department_service.create_department(department_data.model_dump(), tenant_id=tenant_id, created_by=current_user.id)

        department_info = {
            "id": department.id,
            "name": department.name,
            "code": department.code,
            "parent_id": department.parent_id,
            "level": department.level,
            "description": department.description,
            "status": department.status
        }

        return ResponseUtils.success(data=department_info, message="创建部门成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback

        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put(
    "/{department_id}",
    response_model=AuthResponse,
    summary="更新部门信息",
    dependencies=[Depends(permission_dependency("department:update"))]
)
def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新部门信息接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        department_service = DepartmentService(db)
        department = department_service.update_department(department_id, department_data.model_dump(), tenant_id=tenant_id, updated_by=current_user.id)

        department_info = {
            "id": department.id,
            "name": department.name,
            "code": department.code,
            "parent_id": department.parent_id,
            "level": department.level,
            "description": department.description,
            "status": department.status
        }

        return ResponseUtils.success(data=department_info, message="更新部门信息成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback

        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete(
    "/{department_id}",
    response_model=AuthResponse,
    summary="删除部门",
    dependencies=[Depends(permission_dependency("department:delete"))]
)
def delete_department(
    department_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除部门接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        department_service = DepartmentService(db)
        department_service.delete_department(department_id, tenant_id=tenant_id)

        return ResponseUtils.success(message="删除部门成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put(
    "/{department_id}/status",
    response_model=AuthResponse,
    summary="更新部门状态",
    dependencies=[Depends(permission_dependency("department:update"))]
)
def update_department_status(
    department_id: int,
    status: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新部门状态接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        department_service = DepartmentService(db)
        department = department_service.update_department_status(department_id, status, tenant_id=tenant_id, updated_by=current_user.id)

        department_info = {
            "id": department.id,
            "name": department.name,
            "status": department.status
        }

        return ResponseUtils.success(data=department_info, message="更新部门状态成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/{department_id}/children",
    response_model=AuthResponse,
    summary="获取部门的子部门列表",
    dependencies=[Depends(permission_dependency("department:view"))]
)
def get_department_children(
    department_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取部门的子部门列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        department_service = DepartmentService(db)
        children_departments = department_service.get_department_children(department_id, tenant_id=tenant_id)

        children_list = []
        for dept in children_departments:
            children_list.append({
                "id": dept.id,
                "name": dept.name,
                "code": dept.code,
                "parent_id": dept.parent_id,
                "level": dept.level,
                "description": dept.description,
                "status": dept.status
            })

        return ResponseUtils.success(
            data={
                "department_id": department_id,
                "children": children_list
            },
            message="获取子部门列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/{department_id}/users",
    response_model=AuthResponse,
    summary="获取部门用户列表",
    dependencies=[Depends(permission_dependency("department:view"))]
)
def get_department_users(
    department_id: int,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取部门用户列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        department_service = DepartmentService(db)
        users = department_service.get_department_users(department_id, tenant_id=tenant_id, page=page, page_size=page_size)
        total = department_service.count_department_users(department_id, tenant_id=tenant_id)

        return ResponseUtils.pagination(
            data=users,
            total=total,
            page=page,
            page_size=page_size,
            message="获取部门用户列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback

        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/{department_id}/user-count",
    response_model=AuthResponse,
    summary="统计部门用户数量",
    dependencies=[Depends(permission_dependency("department:view"))]
)
def count_department_users(
    department_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """统计部门用户数量接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        department_service = DepartmentService(db)
        user_count = department_service.count_department_users(department_id, tenant_id=tenant_id)

        return ResponseUtils.success(
            data={
                "department_id": department_id,
                "user_count": user_count
            },
            message="统计部门用户数量成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
