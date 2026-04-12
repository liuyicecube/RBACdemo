"""Base Schema"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


class BaseSchema(BaseModel):
    """基础序列化类"""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None


class BaseCreateSchema(BaseModel):
    """基础创建序列化类"""
    pass


class BaseUpdateSchema(BaseModel):
    """基础更新序列化类"""
    pass


class BaseResponse(BaseModel):
    """基础响应模型"""
    code: int = 200
    message: str = "操作成功"
    data: Optional[Any] = None
    metadata: Optional[dict] = None
    timestamp: datetime = datetime.now()


class PaginationResponse(BaseModel):
    """分页响应模型"""
    total: int
    page: int
    page_size: int
    total_pages: int
