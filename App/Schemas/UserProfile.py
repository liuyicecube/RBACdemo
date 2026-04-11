"""User Profile Schema"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class UserProfileBase(BaseModel):
    """用户资料基础模型"""
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别(0:未知,1:男,2:女)")
    birthday: Optional[date] = Field(None, description="生日")
    id_card: Optional[str] = Field(None, max_length=20, description="身份证号")
    address: Optional[str] = Field(None, max_length=255, description="家庭住址")
    emergency_contact: Optional[str] = Field(None, max_length=50, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, max_length=20, description="紧急联系电话")
    position: Optional[str] = Field(None, max_length=50, description="职位")
    entry_date: Optional[date] = Field(None, description="入职日期")
    remark: Optional[str] = Field(None, description="备注")


class UserProfileCreate(UserProfileBase):
    """创建用户资料请求模型"""
    user_id: int = Field(..., description="用户ID")


class UserProfileUpdate(BaseModel):
    """更新用户资料请求模型"""
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别")
    birthday: Optional[date] = Field(None, description="生日")
    id_card: Optional[str] = Field(None, max_length=20, description="身份证号")
    address: Optional[str] = Field(None, max_length=255, description="家庭住址")
    emergency_contact: Optional[str] = Field(None, max_length=50, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, max_length=20, description="紧急联系电话")
    position: Optional[str] = Field(None, max_length=50, description="职位")
    entry_date: Optional[date] = Field(None, description="入职日期")
    remark: Optional[str] = Field(None, description="备注")


class UserProfileResponse(UserProfileBase):
    """用户资料响应模型"""
    id: int = Field(..., description="资料ID")
    user_id: int = Field(..., description="用户ID")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")
    
    model_config = {
        "from_attributes": True
    }


class UserProfileWithUserResponse(UserProfileResponse):
    """用户资料带用户信息响应模型"""
    user: Optional[dict] = Field(None, description="用户信息")
    
    model_config = {
        "from_attributes": True
    }
