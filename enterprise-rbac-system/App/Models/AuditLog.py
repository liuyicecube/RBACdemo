"""Audit Log Model"""

from sqlalchemy import Column, String, Integer, Text, Index
from App.Models.Base import BaseModel


class AuditLogModel(BaseModel):
    """审计日志模型"""

    __tablename__ = "sys_audit_log"
    __table_args__ = (
        Index('idx_audit_table', 'table_name'),
        Index('idx_audit_record', 'table_name', 'record_id'),
        Index('idx_audit_operation', 'operation_type'),
        Index('idx_audit_user', 'user_id'),
        Index('idx_audit_create_time', 'create_time'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    table_name = Column(String(100), nullable=False, comment="表名")
    record_id = Column(Integer, nullable=False, comment="记录ID")
    operation_type = Column(String(20), nullable=False, comment="操作类型(INSERT/UPDATE/DELETE)")
    field_name = Column(String(100), nullable=True, comment="字段名")
    old_value = Column(Text, nullable=True, comment="旧值")
    new_value = Column(Text, nullable=True, comment="新值")
    user_id = Column(Integer, nullable=True, comment="操作用户ID")
    username = Column(String(50), nullable=True, comment="操作用户名")
    change_reason = Column(String(500), nullable=True, comment="变更原因")

    def __repr__(self):
        return f"<AuditLogModel(table={self.table_name}, operation={self.operation_type})>"
