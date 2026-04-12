"""User Session Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class UserSessionBase(BaseModel):
    """用户会话基础模型"""
    user_id: int = Field(..., description="用户ID")
    session_id: str = Field(..., min_length=1, max_length=100, description="会话ID")
    access_token: str = Field(..., min_length=1, max_length=500, description="访问令牌")
    refresh_token: Optional[str] = Field(None, max_length=500, description="刷新令牌")
    device_type: Optional[str] = Field(None, max_length=50, description="设备类型")
    device_info: Optional[str] = Field(None, max_length=500, description="设备信息")
    ip_address: Optional[str] = Field(None, max_length=50, description="IP地址")


class UserSessionCreate(UserSessionBase):
    """创建用户会话请求模型"""
    login_time: datetime = Field(..., description="登录时间")
    last_active_time: datetime = Field(..., description="最后活跃时间")
    expire_time: datetime = Field(..., description="过期时间")


class UserSessionUpdate(BaseModel):
    """更新用户会话请求模型"""
    access_token: Optional[str] = Field(None, min_length=1, max_length=500, description="访问令牌")
    refresh_token: Optional[str] = Field(None, max_length=500, description="刷新令牌")
    last_active_time: Optional[datetime] = Field(None, description="最后活跃时间")
    expire_time: Optional[datetime] = Field(None, description="过期时间")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态")


class UserSessionResponse(BaseModel):
    """用户会话响应模型"""
    id: int = Field(..., description="会话ID")
    user_id: int = Field(..., description="用户ID")
    session_id: str = Field(..., description="会话ID")
    device_type: Optional[str] = Field(None, description="设备类型")
    device_info: Optional[str] = Field(None, description="设备信息")
    ip_address: Optional[str] = Field(None, description="IP地址")
    login_time: datetime = Field(..., description="登录时间")
    last_active_time: datetime = Field(..., description="最后活跃时间")
    expire_time: datetime = Field(..., description="过期时间")
    status: int = Field(..., ge=0, le=1, description="状态(0:已失效,1:有效)")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    model_config = {
        "from_attributes": True
    }


class UserSessionWithUserResponse(UserSessionResponse):
    """用户会话带用户信息响应模型"""
    user: Optional[dict] = Field(None, description="用户信息")

    model_config = {
        "from_attributes": True
    }


class UserSessionListResponse(BaseModel):
    """用户会话列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[UserSessionResponse] = Field(..., description="会话列表")


class UserSessionFilter(BaseModel):
    """用户会话过滤模型"""
    user_id: Optional[int] = Field(None, description="用户ID")
    device_type: Optional[str] = Field(None, description="设备类型")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态")
    keyword: Optional[str] = Field(None, description="搜索关键词")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页记录数")


class KickUserRequest(BaseModel):
    """踢人下线请求模型"""
    session_ids: List[int] = Field(..., description="会话ID列表")
