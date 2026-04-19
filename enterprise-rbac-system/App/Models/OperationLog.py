"""Operation Log Model"""

from sqlalchemy import Column, String, Integer, Text, Index
from App.Models.Base import BaseModel


class OperationLogModel(BaseModel):
    """操作日志模型"""

    __tablename__ = "sys_operation_log"
    __table_args__ = (
        Index('idx_op_log_user', 'user_id'),
        Index('idx_op_log_module', 'module'),
        Index('idx_op_log_create_time', 'create_time'),
        Index('idx_op_log_status', 'status'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, nullable=True, comment="操作用户ID")
    username = Column(String(50), nullable=True, comment="操作用户名")
    module = Column(String(50), nullable=False, comment="模块")
    operation = Column(String(50), nullable=False, comment="操作类型")
    description = Column(String(500), nullable=True, comment="操作描述")
    request_method = Column(String(10), nullable=True, comment="请求方法")
    request_url = Column(String(500), nullable=True, comment="请求URL")
    request_params = Column(Text, nullable=True, comment="请求参数")
    response_result = Column(Text, nullable=True, comment="响应结果")
    execution_time = Column(Integer, nullable=True, comment="执行时长(毫秒)")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(String(500), nullable=True, comment="用户代理")
    status = Column(Integer, default=1, comment="状态(0:失败,1:成功)")
    error_message = Column(String(1000), nullable=True, comment="错误信息")

    def __repr__(self):
        return f"<OperationLogModel(user_id={self.user_id}, module={self.module}, operation={self.operation})>"
