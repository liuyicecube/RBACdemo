"""Audit Log Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AuditLogBase(BaseModel):
    """审计日志基础模型"""
    table_name: Optional[str] = Field(None, max_length=100, description="表名")
    record_id: Optional[int] = Field(None, description="记录ID")
    operation_type: Optional[str] = Field(None, max_length=20, description="操作类型(INSERT/UPDATE/DELETE)")
    old_value: Optional[str] = Field(None, description="旧值")
    new_value: Optional[str] = Field(None, description="新值")
    change_fields: Optional[str] = Field(None, description="变更字段")


class AuditLogCreate(AuditLogBase):
    """创建审计日志请求模型"""
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., max_length=50, description="用户名")


class AuditLogResponse(AuditLogBase):
    """审计日志响应模型"""
    id: int = Field(..., description="日志ID")
    user_id: Optional[int] = Field(None, description="用户ID")
    username: Optional[str] = Field(None, max_length=50, description="用户名")
    create_time: datetime = Field(..., description="创建时间")
    
    model_config = {
        "from_attributes": True
    }


class AuditLogListResponse(BaseModel):
    """审计日志列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[AuditLogResponse] = Field(..., description="日志列表")
