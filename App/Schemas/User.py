"""User Schema"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=6, max_length=20, description="用户名")
    nickname: str = Field(..., min_length=1, max_length=50, description="昵称")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="手机号")
    avatar: Optional[str] = Field(None, description="头像路径")
    department_id: Optional[int] = Field(None, description="所属部门ID")


class UserCreate(UserBase):
    """创建用户请求模型"""
    password: str = Field(..., min_length=6, description="密码")
    status: Optional[int] = Field(1, ge=0, le=1, description="状态(0:禁用,1:启用)")


class UserUpdate(BaseModel):
    """更新用户请求模型"""
    nickname: Optional[str] = Field(None, min_length=1, max_length=50, description="昵称")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="手机号")
    avatar: Optional[str] = Field(None, description="头像路径")
    department_id: Optional[int] = Field(None, description="所属部门ID")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态(0:禁用,1:启用)")
    password: Optional[str] = Field(None, min_length=6, description="密码")


class UserResponse(UserBase):
    """用户响应模型"""
    id: int = Field(..., description="用户ID")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    last_login_time: Optional[str] = Field(None, description="最后登录时间")
    last_login_ip: Optional[str] = Field(None, description="最后登录IP")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    model_config = {
        "from_attributes": True
    }


class UserListResponse(BaseModel):
    """用户列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[UserResponse] = Field(..., description="用户列表")


class UserRoleResponse(BaseModel):
    """用户角色响应模型"""
    id: int = Field(..., description="角色ID")
    name: str = Field(..., description="角色名称")
    code: str = Field(..., description="角色编码")
    type: int = Field(..., ge=0, le=3, description="角色类型(0:系统角色, 1:功能角色, 2:数据角色, 3:自定义角色)")
    is_primary: bool = Field(..., description="是否主角色")

    model_config = {
        "from_attributes": True
    }


class UserRolesResponse(BaseModel):
    """用户角色列表响应模型"""
    user_id: int = Field(..., description="用户ID")
    roles: List[UserRoleResponse] = Field(..., description="角色列表")


class AssignRolesRequest(BaseModel):
    """分配角色请求模型"""
    role_ids: List[int] = Field(..., description="角色ID列表")


class SetPrimaryRoleRequest(BaseModel):
    """设置主角色请求模型"""
    role_id: int = Field(..., description="角色ID")


class UserFilter(BaseModel):
    """用户过滤模型"""
    keyword: Optional[str] = Field(None, description="搜索关键词")
    department_id: Optional[int] = Field(None, description="部门ID")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页记录数")
