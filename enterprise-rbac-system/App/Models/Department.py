"""Department Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from App.Models.Base import BaseModel


class DepartmentModel(BaseModel):
    """部门模型"""

    __tablename__ = "sys_dept"
    __table_args__ = (
        Index('idx_department_parent', 'parent_id'),
        Index('idx_department_leader', 'leader_id'),
        Index('idx_dept_tenant_status', 'tenant_id', 'status'),
        Index('idx_dept_path', 'path'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(50), nullable=False, comment="部门名称")
    code = Column(String(50), unique=True, nullable=False, comment="部门编码")
    parent_id = Column(Integer, ForeignKey("sys_dept.id"), nullable=True, comment="父部门ID")
    leader_id = Column(Integer, ForeignKey("sys_user.id"), nullable=True, comment="部门负责人ID")
    level = Column(Integer, default=1, comment="部门层级")
    path = Column(String(500), nullable=True, comment="部门路径，用逗号分隔的ID，如：1,2,3")
    contact_phone = Column(String(20), nullable=True, comment="联系电话")
    address = Column(String(255), nullable=True, comment="部门地址")
    description = Column(String(255), nullable=True, comment="部门描述")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")

    # 关系定义
    users = relationship("UserModel", back_populates="department", foreign_keys="UserModel.department_id")
    leader = relationship("UserModel", foreign_keys=[leader_id])

    def __repr__(self):
        return f"<DepartmentModel(name={self.name}, code={self.code})>"
