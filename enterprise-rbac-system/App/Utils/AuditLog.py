
"""Audit Log Utils - 审计日志工具类"""

import json
from App.Models.AuditLog import AuditLogModel
from App.Config.Database import SessionLocal


class AuditLogUtils:
    """审计日志工具类"""

    @staticmethod
    def log_audit(
        table_name,
        record_id,
        operation_type,
        field_name=None,
        old_value=None,
        new_value=None,
        user_id=None,
        username=None,
        change_reason=None
    ):
        """
        记录审计日志

        Args:
            table_name: 表名
            record_id: 记录ID
            operation_type: 操作类型 (INSERT/UPDATE/DELETE)
            field_name: 字段名
            old_value: 旧值
            new_value: 新值
            user_id: 用户ID
            username: 用户名
            change_reason: 变更原因
        """
        try:
            db = SessionLocal()
            
            old_value_str = None
            if old_value is not None:
                if isinstance(old_value, (dict, list)):
                    old_value_str = json.dumps(old_value, ensure_ascii=False)
                else:
                    old_value_str = str(old_value)
            
            new_value_str = None
            if new_value is not None:
                if isinstance(new_value, (dict, list)):
                    new_value_str = json.dumps(new_value, ensure_ascii=False)
                else:
                    new_value_str = str(new_value)
            
            log = AuditLogModel(
                table_name=table_name,
                record_id=record_id,
                operation_type=operation_type,
                field_name=field_name,
                old_value=old_value_str,
                new_value=new_value_str,
                user_id=user_id,
                username=username,
                change_reason=change_reason
            )
            db.add(log)
            db.commit()
        except Exception as e:
            print(f"[AuditLog] Failed to save audit log: {e}")
            if 'db' in locals():
                db.rollback()
        finally:
            if 'db' in locals():
                db.close()

    @staticmethod
    def log_create(
        table_name,
        record_id,
        new_data,
        user_id=None,
        username=None,
        change_reason=None
    ):
        """记录创建操作"""
        AuditLogUtils.log_audit(
            table_name=table_name,
            record_id=record_id,
            operation_type="INSERT",
            field_name=None,
            old_value=None,
            new_value=new_data,
            user_id=user_id,
            username=username,
            change_reason=change_reason
        )

    @staticmethod
    def log_update(
        table_name,
        record_id,
        old_data,
        new_data,
        user_id=None,
        username=None,
        change_reason=None
    ):
        """记录更新操作（逐个字段记录）"""
        all_keys = set(old_data.keys()).union(set(new_data.keys()))
        
        for key in all_keys:
            old_val = old_data.get(key)
            new_val = new_data.get(key)
            
            if old_val != new_val:
                AuditLogUtils.log_audit(
                    table_name=table_name,
                    record_id=record_id,
                    operation_type="UPDATE",
                    field_name=key,
                    old_value=old_val,
                    new_value=new_val,
                    user_id=user_id,
                    username=username,
                    change_reason=change_reason
                )

    @staticmethod
    def log_delete(
        table_name,
        record_id,
        old_data,
        user_id=None,
        username=None,
        change_reason=None
    ):
        """记录删除操作"""
        AuditLogUtils.log_audit(
            table_name=table_name,
            record_id=record_id,
            operation_type="DELETE",
            field_name=None,
            old_value=old_data,
            new_value=None,
            user_id=user_id,
            username=username,
            change_reason=change_reason
        )

