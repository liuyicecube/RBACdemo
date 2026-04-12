"""System Dict Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SystemDictItemBase(BaseModel):
    """字典项基础模型"""
    label: str = Field(..., min_length=1, max_length=100, description="标签")
    value: str = Field(..., min_length=1, max_length=100, description="值")
    color: Optional[str] = Field(None, max_length=50, description="颜色")
    sort: Optional[int] = Field(0, description="排序")
    description: Optional[str] = Field(None, max_length=500, description="描述")


class SystemDictItemCreate(SystemDictItemBase):
    """创建字典项请求模型"""
    status: Optional[int] = Field(1, ge=0, le=1, description="状态(0:禁用,1:启用)")


class SystemDictItemUpdate(BaseModel):
    """更新字典项请求模型"""
    label: Optional[str] = Field(None, min_length=1, max_length=100, description="标签")
    value: Optional[str] = Field(None, min_length=1, max_length=100, description="值")
    color: Optional[str] = Field(None, max_length=50, description="颜色")
    sort: Optional[int] = Field(None, description="排序")
    description: Optional[str] = Field(None, max_length=500, description="描述")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态(0:禁用,1:启用)")


class SystemDictItemResponse(SystemDictItemBase):
    """字典项响应模型"""
    id: int = Field(..., description="字典项ID")
    dict_id: int = Field(..., description="字典ID")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    model_config = {
        "from_attributes": True
    }


class SystemDictBase(BaseModel):
    """字典基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="字典名称")
    code: str = Field(..., min_length=1, max_length=100, description="字典编码")
    description: Optional[str] = Field(None, max_length=500, description="描述")
    sort: Optional[int] = Field(0, description="排序")


class SystemDictCreate(SystemDictBase):
    """创建字典请求模型"""
    status: Optional[int] = Field(1, ge=0, le=1, description="状态(0:禁用,1:启用)")


class SystemDictUpdate(BaseModel):
    """更新字典请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="字典名称")
    code: Optional[str] = Field(None, min_length=1, max_length=100, description="字典编码")
    description: Optional[str] = Field(None, max_length=500, description="描述")
    sort: Optional[int] = Field(None, description="排序")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态(0:禁用,1:启用)")


class SystemDictResponse(SystemDictBase):
    """字典响应模型"""
    id: int = Field(..., description="字典ID")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    model_config = {
        "from_attributes": True
    }


class SystemDictWithItemsResponse(SystemDictResponse):
    """字典带字典项响应模型"""
    items: List[SystemDictItemResponse] = Field([], description="字典项列表")

    model_config = {
        "from_attributes": True
    }


class SystemDictListResponse(BaseModel):
    """字典列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[SystemDictResponse] = Field(..., description="字典列表")
