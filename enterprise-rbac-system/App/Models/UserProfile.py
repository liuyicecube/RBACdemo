"""User Profile Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Date, Text, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class UserProfileModel(BaseModel):
    """用户扩展信息模型"""

    __tablename__ = "sys_user_profile"
    __table_args__ = (
        Index('idx_profile_user', 'user_id'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, ForeignKey("sys_user.id"), unique=True, nullable=False, comment="用户ID")
    gender = Column(Integer, nullable=True, comment="性别(0:未知,1:男,2:女)")
    birthday = Column(Date, nullable=True, comment="生日")
    id_card = Column(String(20), nullable=True, comment="身份证号")
    address = Column(String(255), nullable=True, comment="家庭住址")
    emergency_contact = Column(String(50), nullable=True, comment="紧急联系人")
    emergency_phone = Column(String(20), nullable=True, comment="紧急联系电话")
    position = Column(String(50), nullable=True, comment="职位")
    entry_date = Column(Date, nullable=True, comment="入职日期")
    remark = Column(Text, nullable=True, comment="备注")

    user = relationship("UserModel", back_populates="profile")

    def __repr__(self):
        return f"<UserProfileModel(user_id={self.user_id})>"
