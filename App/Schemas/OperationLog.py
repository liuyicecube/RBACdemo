"""Operation Log Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class OperationLogBase(BaseModel):
    """操作日志基础模型"""
    module: Optional[str] = Field(None, max_length=50, description="模块名称")
    operation: Optional[str] = Field(None, max_length=50, description="操作类型")
    method: Optional[str] = Field(None, max_length=20, description="请求方法")
    url: Optional[str] = Field(None, max_length=255, description="请求URL")
    ip: Optional[str] = Field(None, max_length=50, description="IP地址")
    params: Optional[str] = Field(None, description="请求参数")
    result: Optional[str] = Field(None, description="响应结果")
    status: Optional[int] = Field(1, ge=0, le=1, description="状态(0:失败,1:成功)")
    error_msg: Optional[str] = Field(None, max_length=1000, description="错误信息")
    execution_time: Optional[int] = Field(None, description="执行时间(ms)")


class OperationLogCreate(OperationLogBase):
    """创建操作日志请求模型"""
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., max_length=50, description="用户名")


class OperationLogResponse(OperationLogBase):
    """操作日志响应模型"""
    id: int = Field(..., description="日志ID")
    user_id: Optional[int] = Field(None, description="用户ID")
    username: Optional[str] = Field(None, max_length=50, description="用户名")
    create_time: datetime = Field(..., description="创建时间")

    model_config = {
        "from_attributes": True
    }


class OperationLogListResponse(BaseModel):
    """操作日志列表响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")
    data: List[OperationLogResponse] = Field(..., description="日志列表")
