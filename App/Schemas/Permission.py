"""Permission Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PermissionBase(BaseModel):
    """权限基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="权限名称")
    code: str = Field(..., min_length=1, max_length=50, description="权限编码")
    type: int = Field(..., ge=0, le=4, description="权限类型(0:菜单, 1:按钮, 2:API, 3:数据, 4:字段)")
    resource_type: str = Field(..., min_length=1, max_length=50, description="资源类型")
    resource_id: Optional[str] = Field(None, max_length=100, description="资源ID")
    action: str = Field(..., description="操作类型(view, create, update, delete, export)")
    path: Optional[str] = Field(None, max_length=255, description="访问路径(API路径或菜单路径)")
    method: Optional[str] = Field(None, max_length=10, description="请求方法(GET, POST, PUT, DELETE等)")
    parent_id: Optional[int] = Field(None, description="父权限ID")
    description: Optional[str] = Field(None, max_length=255, description="权限描述")


class PermissionCreate(PermissionBase):
    """创建权限请求模型"""
    status: Optional[int] = Field(1, ge=0, le=1, description="状态(0:禁用,1:启用)")


class PermissionUpdate(BaseModel):
    """更新权限请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="权限名称")
    code: Optional[str] = Field(None, min_length=1, max_length=50, description="权限编码")
    type: Optional[int] = Field(None, ge=0, le=4, description="权限类型(0:菜单, 1:按钮, 2:API, 3:数据, 4:字段)")
    resource_type: Optional[str] = Field(None, min_length=1, max_length=50, description="资源类型")
    resource_id: Optional[str] = Field(None, max_length=100, description="资源ID")
    action: Optional[str] = Field(None, description="操作类型(view, create, update, delete, export)")
    path: Optional[str] = Field(None, max_length=255, description="访问路径(API路径或菜单路径)")
    method: Optional[str] = Field(None, max_length=10, description="请求方法(GET, POST, PUT, DELETE等)")
    parent_id: Optional[int] = Field(None, description="父权限ID")
    description: Optional[str] = Field(None, max_length=255, description="权限描述")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态(0:禁用,1:启用)")


class PermissionResponse(PermissionBase):
    """权限响应模型"""
    id: int = Field(..., description="权限ID")
    level: int = Field(..., ge=1, description="权限层级")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")
    
    model_config = {
        "from_attributes": True
    }


class PermissionListResponse(BaseModel):
    """权限列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[PermissionResponse] = Field(..., description="权限列表")


class PermissionRoleResponse(BaseModel):
    """权限角色响应模型"""
    id: int = Field(..., description="角色ID")
    name: str = Field(..., description="角色名称")
    code: str = Field(..., description="角色编码")
    type: int = Field(..., ge=0, le=3, description="角色类型(0:系统角色, 1:功能角色, 2:数据角色, 3:自定义角色)")
    description: Optional[str] = Field(None, description="角色描述")
    
    model_config = {
        "from_attributes": True
    }


class PermissionRolesResponse(BaseModel):
    """权限角色列表响应模型"""
    permission_id: int = Field(..., description="权限ID")
    roles: List[PermissionRoleResponse] = Field(..., description="角色列表")


class PermissionFilter(BaseModel):
    """权限过滤模型"""
    keyword: Optional[str] = Field(None, description="搜索关键词")
    type: Optional[int] = Field(None, ge=0, le=4, description="权限类型")
    resource_type: Optional[str] = Field(None, description="资源类型")
    action: Optional[str] = Field(None, description="操作类型")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态")
    parent_id: Optional[int] = Field(None, description="父权限ID")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页记录数")