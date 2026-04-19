"""Authentication API"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from App.Schemas.Auth import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    ChangePasswordRequest,
    ResetPasswordRequest,
    AuthResponse
)
from App.Services.AuthService import AuthService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user, get_current_user_and_tenant_id
from App.Models.User import UserModel
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/auth",
    tags=["认证管理"]
)


@router.post("/login", response_model=AuthResponse, summary="用户登录")
def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
) -> JSONResponse:
    """用户登录接口"""
    try:
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")

        auth_service = AuthService(db)
        login_result = auth_service.login(
            username=login_data.username,
            password=login_data.password,
            ip=client_ip,
            device_type="web",
            device_info=user_agent
        )

        return ResponseUtils.success(data=login_result, message="登录成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("/register", response_model=AuthResponse, summary="用户注册")
def register(
    register_data: RegisterRequest,
    tenant_id: int = 1,
    db: Session = Depends(get_db)
) -> JSONResponse:
    """用户注册接口"""
    try:
        auth_service = AuthService(db)
        user = auth_service.register(
            username=register_data.username,
            password=register_data.password,
            nickname=register_data.nickname,
            tenant_id=tenant_id,
            email=register_data.email,
            phone=register_data.phone
        )

        return ResponseUtils.success(data={
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "phone": user.phone
        }, message="注册成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("/refresh", response_model=AuthResponse, summary="刷新Token")
def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
) -> JSONResponse:
    """刷新Token接口"""
    try:
        auth_service = AuthService(db)
        refresh_result = auth_service.refresh_token(
            refresh_token=refresh_data.refresh_token
        )

        return ResponseUtils.success(data=refresh_result, message="Token刷新成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("/change-password", response_model=AuthResponse, summary="修改密码")
def change_password(
    password_data: ChangePasswordRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> JSONResponse:
    """修改密码接口"""
    try:
        auth_service = AuthService(db)
        auth_service.change_password(
            user_id=current_user.id,
            old_password=password_data.old_password,
            new_password=password_data.new_password,
            tenant_id=current_user.tenant_id
        )

        return ResponseUtils.success(data=None, message="密码修改成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("/reset-password", response_model=AuthResponse, summary="重置密码")
def reset_password(
    password_data: ResetPasswordRequest,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> JSONResponse:
    """重置密码接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        auth_service = AuthService(db)
        auth_service.reset_password(
            user_id=password_data.user_id,
            new_password=password_data.new_password,
            tenant_id=tenant_id,
            updated_by=current_user.id
        )

        return ResponseUtils.success(data=None, message="密码重置成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/profile", response_model=AuthResponse, summary="获取用户信息")
def get_profile(
    current_user: UserModel = Depends(get_current_user)
) -> JSONResponse:
    """获取当前用户信息接口"""
    try:
        user_info = {
            "id": current_user.id,
            "username": current_user.username,
            "nickname": current_user.nickname,
            "email": current_user.email,
            "phone": current_user.phone,
            "avatar": current_user.avatar,
            "department_id": current_user.department_id,
            "tenant_id": current_user.tenant_id,
            "status": current_user.status,
            "last_login_time": current_user.last_login_time.isoformat() if hasattr(current_user.last_login_time, 'isoformat') else None,
            "last_login_ip": current_user.last_login_ip
        }

        return ResponseUtils.success(data=user_info, message="获取用户信息成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("/logout", summary="退出登录")
def logout() -> JSONResponse:
    """用户退出登录接口"""
    try:
        return ResponseUtils.success(data=None, message="退出登录成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
