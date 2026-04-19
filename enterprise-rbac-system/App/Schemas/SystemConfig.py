"""System Config Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SystemConfigBase(BaseModel):
    """配置基础模型"""
    config_key: str = Field(..., min_length=1, max_length=100, description="配置键")
    config_value: Optional[str] = Field(None, description="配置值")
    config_type: Optional[str] = Field("string", max_length=20, description="配置类型(string,int,bool,json)")
    description: Optional[str] = Field(None, max_length=255, description="配置描述")
    group_name: Optional[str] = Field(None, max_length=50, description="配置分组")
    is_system: Optional[int] = Field(0, ge=0, le=1, description="是否系统配置(0:否,1:是)")
    sort: Optional[int] = Field(0, description="排序")


class SystemConfigCreate(SystemConfigBase):
    """创建配置请求模型"""
    status: Optional[int] = Field(1, ge=0, le=1, description="状态(0:禁用,1:启用)")


class SystemConfigUpdate(BaseModel):
    """更新配置请求模型"""
    config_value: Optional[str] = Field(None, description="配置值")
    config_type: Optional[str] = Field(None, max_length=20, description="配置类型")
    description: Optional[str] = Field(None, max_length=255, description="配置描述")
    group_name: Optional[str] = Field(None, max_length=50, description="配置分组")
    is_system: Optional[int] = Field(None, ge=0, le=1, description="是否系统配置")
    sort: Optional[int] = Field(None, description="排序")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态(0:禁用,1:启用)")


class SystemConfigResponse(SystemConfigBase):
    """配置响应模型"""
    id: int = Field(..., description="配置ID")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    model_config = {
        "from_attributes": True
    }


class SystemConfigListResponse(BaseModel):
    """配置列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[SystemConfigResponse] = Field(..., description="配置列表")


class SystemConfigGroupResponse(BaseModel):
    """分组配置响应模型"""
    group: str = Field(..., description="分组名称")
    configs: List[SystemConfigResponse] = Field(..., description="配置列表")


class BatchUpdateConfigsRequest(BaseModel):
    """批量更新配置请求模型"""
    model_config = {
        "extra": "allow"
    }
