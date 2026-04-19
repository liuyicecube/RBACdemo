"""Authentication Schema"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Any
from datetime import datetime


class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str = Field(..., min_length=5, max_length=20, description="用户名")
    password: str = Field(..., min_length=6, description="密码")


class RegisterRequest(BaseModel):
    """注册请求模型"""
    username: str = Field(..., min_length=5, max_length=20, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    nickname: str = Field(..., min_length=1, max_length=50, description="昵称")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="手机号")


class RefreshTokenRequest(BaseModel):
    """刷新Token请求模型"""
    refresh_token: str = Field(..., description="刷新Token")


class ChangePasswordRequest(BaseModel):
    """修改密码请求模型"""
    old_password: str = Field(..., min_length=6, description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")


class ResetPasswordRequest(BaseModel):
    """重置密码请求模型"""
    user_id: int = Field(..., description="用户ID")
    new_password: str = Field(..., min_length=6, description="新密码")


class TokenResponse(BaseModel):
    """Token响应模型"""
    access_token: str = Field(..., description="访问Token")
    refresh_token: Optional[str] = Field(None, description="刷新Token")
    token_type: str = Field("bearer", description="Token类型")


class UserInfoResponse(BaseModel):
    """用户信息响应模型"""
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    nickname: str = Field(..., description="昵称")
    email: Optional[str] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="手机号")
    avatar: Optional[str] = Field(None, description="头像路径")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    status: int = Field(..., description="状态(0:禁用,1:启用)")
    last_login_time: Optional[str] = Field(None, description="最后登录时间")
    last_login_ip: Optional[str] = Field(None, description="最后登录IP")


class LoginResponse(BaseModel):
    """登录响应模型"""
    access_token: str = Field(..., description="访问Token")
    refresh_token: str = Field(..., description="刷新Token")
    token_type: str = Field("bearer", description="Token类型")
    user: UserInfoResponse = Field(..., description="用户信息")


class AuthResponse(BaseModel):
    """认证响应模型"""
    code: int = Field(200, description="响应码")
    message: str = Field("操作成功", description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")
    timestamp: datetime = Field(datetime.now(), description="响应时间")
