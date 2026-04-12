"""User Profile Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from App.Schemas.UserProfile import UserProfileCreate, UserProfileUpdate
from App.Schemas.Auth import AuthResponse
from App.Services.UserProfileService import UserProfileService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency

from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/user-profiles",
    tags=["用户资料管理"]
)


@router.get("/user/{user_id}", response_model=AuthResponse, summary="获取指定用户的资料", dependencies=[Depends(permission_dependency("user_profile:view"))])
def get_user_profile_by_user_id(
    user_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取指定用户的资料接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        profile_service = UserProfileService(db)
        profile = profile_service.get_profile_by_user_id(user_id, tenant_id=tenant_id)

        if not profile:
            return ResponseUtils.success(data=None, message="用户资料不存在")

        profile_info = {
            "id": profile.id,
            "user_id": profile.user_id,
            "gender": profile.gender,
            "birthday": profile.birthday.isoformat() if hasattr(profile.birthday, 'isoformat') else profile.birthday,
            "id_card": profile.id_card,
            "address": profile.address,
            "emergency_contact": profile.emergency_contact,
            "emergency_phone": profile.emergency_phone,
            "position": profile.position,
            "entry_date": profile.entry_date.isoformat() if hasattr(profile.entry_date, 'isoformat') else profile.entry_date,
            "remark": profile.remark,
            "create_time": profile.create_time.isoformat() if hasattr(profile.create_time, 'isoformat') else profile.create_time,
            "update_time": profile.update_time.isoformat() if hasattr(profile.update_time, 'isoformat') else profile.update_time
        }

        return ResponseUtils.success(data=profile_info, message="获取用户资料成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_user_profile_by_user_id: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/my", response_model=AuthResponse, summary="获取当前登录用户的资料", dependencies=[Depends(permission_dependency("user_profile:view"))])
def get_my_profile(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取当前登录用户的资料接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        profile_service = UserProfileService(db)
        profile = profile_service.get_profile_by_user_id(current_user.id, tenant_id=tenant_id)

        if not profile:
            return ResponseUtils.success(data=None, message="用户资料不存在")

        profile_info = {
            "id": profile.id,
            "user_id": profile.user_id,
            "gender": profile.gender,
            "birthday": profile.birthday.isoformat() if hasattr(profile.birthday, 'isoformat') else profile.birthday,
            "id_card": profile.id_card,
            "address": profile.address,
            "emergency_contact": profile.emergency_contact,
            "emergency_phone": profile.emergency_phone,
            "position": profile.position,
            "entry_date": profile.entry_date.isoformat() if hasattr(profile.entry_date, 'isoformat') else profile.entry_date,
            "remark": profile.remark,
            "create_time": profile.create_time.isoformat() if hasattr(profile.create_time, 'isoformat') else profile.create_time,
            "update_time": profile.update_time.isoformat() if hasattr(profile.update_time, 'isoformat') else profile.update_time
        }

        return ResponseUtils.success(data=profile_info, message="获取用户资料成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("", response_model=AuthResponse, summary="创建用户资料", dependencies=[Depends(permission_dependency("user_profile:create"))])
def create_user_profile(
    profile_data: UserProfileCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建用户资料接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        profile_service = UserProfileService(db)

        profile = profile_service.create_profile(profile_data.model_dump(), tenant_id=tenant_id, created_by=current_user.id)

        profile_info = {
            "id": profile.id,
            "user_id": profile.user_id,
            "gender": profile.gender,
            "position": profile.position
        }

        return ResponseUtils.success(data=profile_info, message="创建用户资料成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in create_user_profile: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/user/{user_id}", response_model=AuthResponse, summary="更新指定用户的资料", dependencies=[Depends(permission_dependency("user_profile:update"))])
def update_user_profile(
    user_id: int,
    profile_data: UserProfileUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新指定用户的资料接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        profile_service = UserProfileService(db)
        profile = profile_service.update_profile(user_id, profile_data.model_dump(exclude_unset=True), tenant_id=tenant_id, updated_by=current_user.id)

        profile_info = {
            "id": profile.id,
            "user_id": profile.user_id,
            "gender": profile.gender,
            "position": profile.position
        }

        return ResponseUtils.success(data=profile_info, message="更新用户资料成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in update_user_profile: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/my", response_model=AuthResponse, summary="更新当前登录用户的资料", dependencies=[Depends(permission_dependency("user_profile:update"))])
def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新当前登录用户的资料接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        profile_service = UserProfileService(db)
        profile = profile_service.update_profile(current_user.id, profile_data.model_dump(exclude_unset=True), tenant_id=tenant_id, updated_by=current_user.id)

        profile_info = {
            "id": profile.id,
            "user_id": profile.user_id,
            "gender": profile.gender,
            "position": profile.position
        }

        return ResponseUtils.success(data=profile_info, message="更新用户资料成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in update_my_profile: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/user/{user_id}", response_model=AuthResponse, summary="删除指定用户的资料", dependencies=[Depends(permission_dependency("user_profile:delete"))])
def delete_user_profile(
    user_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除指定用户的资料接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        profile_service = UserProfileService(db)
        profile_service.delete_profile_by_user_id(user_id, tenant_id=tenant_id)

        return ResponseUtils.success(message="删除用户资料成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
