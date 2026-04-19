"""Department Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DepartmentBase(BaseModel):
    """部门基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="部门名称")
    code: str = Field(..., min_length=1, max_length=50, description="部门编码")
    parent_id: Optional[int] = Field(None, description="父部门ID")
    leader_id: Optional[int] = Field(None, description="部门负责人ID")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    address: Optional[str] = Field(None, max_length=255, description="部门地址")
    description: Optional[str] = Field(None, max_length=255, description="部门描述")


class DepartmentCreate(DepartmentBase):
    """创建部门请求模型"""
    status: Optional[int] = Field(1, ge=0, le=1, description="状态(0:禁用,1:启用)")


class DepartmentUpdate(BaseModel):
    """更新部门请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="部门名称")
    code: Optional[str] = Field(None, min_length=1, max_length=50, description="部门编码")
    parent_id: Optional[int] = Field(None, description="父部门ID")
    leader_id: Optional[int] = Field(None, description="部门负责人ID")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    address: Optional[str] = Field(None, max_length=255, description="部门地址")
    description: Optional[str] = Field(None, max_length=255, description="部门描述")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态(0:禁用,1:启用)")


class DepartmentResponse(DepartmentBase):
    """部门响应模型"""
    id: int = Field(..., description="部门ID")
    level: int = Field(..., ge=1, description="部门层级")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    model_config = {
        "from_attributes": True
    }


class DepartmentListResponse(BaseModel):
    """部门列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[DepartmentResponse] = Field(..., description="部门列表")


class DepartmentTreeResponse(BaseModel):
    """部门树响应模型"""
    id: int = Field(..., description="部门ID")
    name: str = Field(..., description="部门名称")
    code: str = Field(..., description="部门编码")
    parent_id: Optional[int] = Field(None, description="父部门ID")
    level: int = Field(..., ge=1, description="部门层级")
    description: Optional[str] = Field(None, description="部门描述")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    children: Optional[List["DepartmentTreeResponse"]] = Field([], description="子部门列表")

    model_config = {
        "from_attributes": True
    }


class DepartmentFilter(BaseModel):
    """部门过滤模型"""
    keyword: Optional[str] = Field(None, description="搜索关键词")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态")
    parent_id: Optional[int] = Field(None, description="父部门ID")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页记录数")


# 更新模型引用
DepartmentTreeResponse.model_rebuild()
