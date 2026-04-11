"""Menu Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MenuBase(BaseModel):
    """菜单基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="菜单名称")
    code: str = Field(..., min_length=1, max_length=50, description="菜单编码")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    type: int = Field(..., ge=0, le=4, description="菜单类型(0:目录,1:菜单,2:按钮,3:内嵌,4:外链)")
    path: Optional[str] = Field(None, max_length=255, description="访问路径")
    component: Optional[str] = Field(None, max_length=255, description="组件路径")
    icon: Optional[str] = Field(None, max_length=50, description="菜单图标")
    sort: Optional[int] = Field(0, description="排序")


class MenuCreate(MenuBase):
    """创建菜单请求模型"""
    status: Optional[int] = Field(1, ge=0, le=1, description="状态(0:禁用,1:启用)")


class MenuUpdate(BaseModel):
    """更新菜单请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="菜单名称")
    code: Optional[str] = Field(None, min_length=1, max_length=50, description="菜单编码")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    type: Optional[int] = Field(None, ge=0, le=4, description="菜单类型(0:目录,1:菜单,2:按钮,3:内嵌,4:外链)")
    path: Optional[str] = Field(None, max_length=255, description="访问路径")
    component: Optional[str] = Field(None, max_length=255, description="组件路径")
    icon: Optional[str] = Field(None, max_length=50, description="菜单图标")
    sort: Optional[int] = Field(None, description="排序")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态(0:禁用,1:启用)")


class MenuResponse(MenuBase):
    """菜单响应模型"""
    id: int = Field(..., description="菜单ID")
    level: int = Field(..., ge=1, description="菜单层级")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")
    
    model_config = {
        "from_attributes": True
    }


class MenuListResponse(BaseModel):
    """菜单列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[MenuResponse] = Field(..., description="菜单列表")


class MenuTreeResponse(BaseModel):
    """菜单树响应模型"""
    id: int = Field(..., description="菜单ID")
    name: str = Field(..., description="菜单名称")
    code: str = Field(..., description="菜单编码")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    level: int = Field(..., ge=1, description="菜单层级")
    type: int = Field(..., ge=0, le=4, description="菜单类型(0:目录,1:菜单,2:按钮,3:内嵌,4:外链)")
    path: Optional[str] = Field(None, description="访问路径")
    component: Optional[str] = Field(None, description="组件路径")
    icon: Optional[str] = Field(None, description="菜单图标")
    sort: int = Field(..., description="排序")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    children: Optional[List["MenuTreeResponse"]] = Field([], description="子菜单列表")
    
    model_config = {
        "from_attributes": True
    }


class MenuFilter(BaseModel):
    """菜单过滤模型"""
    keyword: Optional[str] = Field(None, description="搜索关键词")
    type: Optional[int] = Field(None, ge=0, le=4, description="菜单类型")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页记录数")


# 更新模型引用
MenuTreeResponse.model_rebuild()