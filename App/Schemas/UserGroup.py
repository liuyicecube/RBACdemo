"""User Group Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class UserGroupBase(BaseModel):
    """用户组基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="用户组名称")
    code: str = Field(..., min_length=1, max_length=100, description="用户组编码")
    description: Optional[str] = Field(None, max_length=500, description="描述")
    sort: int = Field(0, ge=0, description="排序")


class UserGroupCreate(UserGroupBase):
    """创建用户组请求模型"""
    status: Optional[int] = Field(1, ge=0, le=1, description="状态(0:禁用,1:启用)")


class UserGroupUpdate(BaseModel):
    """更新用户组请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="用户组名称")
    code: Optional[str] = Field(None, min_length=1, max_length=100, description="用户组编码")
    description: Optional[str] = Field(None, max_length=500, description="描述")
    sort: Optional[int] = Field(None, ge=0, description="排序")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态(0:禁用,1:启用)")


class UserGroupResponse(UserGroupBase):
    """用户组响应模型"""
    id: int = Field(..., description="用户组ID")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    model_config = {
        "from_attributes": True
    }


class UserGroupListResponse(BaseModel):
    """用户组列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[UserGroupResponse] = Field(..., description="用户组列表")


class UserGroupWithUsersResponse(UserGroupResponse):
    """用户组带用户列表响应模型"""
    users: List[dict] = Field([], description="用户列表")

    model_config = {
        "from_attributes": True
    }


class UserGroupWithRolesResponse(UserGroupResponse):
    """用户组带角色列表响应模型"""
    roles: List[dict] = Field([], description="角色列表")

    model_config = {
        "from_attributes": True
    }


class AssignUsersRequest(BaseModel):
    """分配用户请求模型"""
    user_ids: List[int] = Field(..., description="用户ID列表")


class AssignRolesRequest(BaseModel):
    """分配角色请求模型"""
    role_ids: List[int] = Field(..., description="角色ID列表")


class UserGroupFilter(BaseModel):
    """用户组过滤模型"""
    keyword: Optional[str] = Field(None, description="搜索关键词")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页记录数")
