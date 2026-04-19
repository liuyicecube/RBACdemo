"""Data Permission Rule Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DataPermissionRuleBase(BaseModel):
    """数据权限规则基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="规则名称")
    code: str = Field(..., min_length=1, max_length=100, description="规则编码")
    permission_id: int = Field(..., description="关联权限ID")
    resource_table: str = Field(..., min_length=1, max_length=100, description="资源表名")
    rule_type: int = Field(..., ge=0, le=4, description="规则类型(0:全部,1:本部门,2:本部门及下级,3:仅本人,4:自定义)")
    rule_expression: Optional[str] = Field(None, description="自定义规则表达式(SQL WHERE片段)")
    description: Optional[str] = Field(None, max_length=500, description="规则描述")


class DataPermissionRuleCreate(DataPermissionRuleBase):
    """创建数据权限规则请求模型"""
    status: Optional[int] = Field(1, ge=0, le=1, description="状态(0:禁用,1:启用)")


class DataPermissionRuleUpdate(BaseModel):
    """更新数据权限规则请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="规则名称")
    code: Optional[str] = Field(None, min_length=1, max_length=100, description="规则编码")
    permission_id: Optional[int] = Field(None, description="关联权限ID")
    resource_table: Optional[str] = Field(None, min_length=1, max_length=100, description="资源表名")
    rule_type: Optional[int] = Field(None, ge=0, le=4, description="规则类型")
    rule_expression: Optional[str] = Field(None, description="自定义规则表达式")
    description: Optional[str] = Field(None, max_length=500, description="规则描述")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态")


class DataPermissionRuleResponse(DataPermissionRuleBase):
    """数据权限规则响应模型"""
    id: int = Field(..., description="规则ID")
    status: int = Field(..., ge=0, le=1, description="状态(0:禁用,1:启用)")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    model_config = {
        "from_attributes": True
    }


class DataPermissionRuleListResponse(BaseModel):
    """数据权限规则列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[DataPermissionRuleResponse] = Field(..., description="规则列表")


class DataPermissionRuleWithPermissionResponse(DataPermissionRuleResponse):
    """数据权限规则带权限信息响应模型"""
    permission: Optional[dict] = Field(None, description="关联权限信息")

    model_config = {
        "from_attributes": True
    }


class DataPermissionRuleFilter(BaseModel):
    """数据权限规则过滤模型"""
    keyword: Optional[str] = Field(None, description="搜索关键词")
    permission_id: Optional[int] = Field(None, description="权限ID")
    rule_type: Optional[int] = Field(None, ge=0, le=4, description="规则类型")
    status: Optional[int] = Field(None, ge=0, le=1, description="状态")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页记录数")
