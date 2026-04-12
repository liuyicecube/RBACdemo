"""Initialize System Configs"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from App.Core.Database import SessionLocal
from App.Models.SystemConfig import SystemConfigModel


def init_system_configs():
    """初始化系统配置"""
    db: Session = SessionLocal()
    try:
        default_configs = [
            {
                "config_key": "app_name",
                "config_value": "Enterprise RBAC System",
                "config_type": "string",
                "group_name": "basic",
                "description": "应用名称",
                "is_system": 1,
                "status": 1,
                "sort": 1
            },
            {
                "config_key": "app_version",
                "config_value": "1.0.0",
                "config_type": "string",
                "group_name": "basic",
                "description": "应用版本",
                "is_system": 1,
                "status": 1,
                "sort": 2
            },
            {
                "config_key": "jwt_access_token_expire_minutes",
                "config_value": "30",
                "config_type": "int",
                "group_name": "security",
                "description": "JWT访问令牌过期时间（分钟）",
                "is_system": 1,
                "status": 1,
                "sort": 1
            },
            {
                "config_key": "jwt_refresh_token_expire_days",
                "config_value": "7",
                "config_type": "int",
                "group_name": "security",
                "description": "JWT刷新令牌过期时间（天）",
                "is_system": 1,
                "status": 1,
                "sort": 2
            },
            {
                "config_key": "password_salt_length",
                "config_value": "16",
                "config_type": "int",
                "group_name": "security",
                "description": "密码盐值长度",
                "is_system": 1,
                "status": 1,
                "sort": 3
            },
            {
                "config_key": "bcrypt_rounds",
                "config_value": "12",
                "config_type": "int",
                "group_name": "security",
                "description": "Bcrypt加密轮数",
                "is_system": 1,
                "status": 1,
                "sort": 4
            },
            {
                "config_key": "upload_dir",
                "config_value": "./uploads",
                "config_type": "string",
                "group_name": "upload",
                "description": "上传文件存储目录",
                "is_system": 1,
                "status": 1,
                "sort": 1
            },
            {
                "config_key": "max_file_size",
                "config_value": "5242880",
                "config_type": "int",
                "group_name": "upload",
                "description": "最大文件大小（字节，默认5MB）",
                "is_system": 1,
                "status": 1,
                "sort": 2
            },
            {
                "config_key": "allowed_image_extensions",
                "config_value": "png,jpg,jpeg,gif",
                "config_type": "string",
                "group_name": "upload",
                "description": "允许的图片扩展名",
                "is_system": 1,
                "status": 1,
                "sort": 3
            },
            {
                "config_key": "cors_origins",
                "config_value": "http://localhost:3000,http://localhost:8080,http://localhost:5175",
                "config_type": "string",
                "group_name": "cors",
                "description": "CORS允许的源地址",
                "is_system": 1,
                "status": 1,
                "sort": 1
            },
            {
                "config_key": "log_level",
                "config_value": "INFO",
                "config_type": "string",
                "group_name": "log",
                "description": "日志级别",
                "is_system": 1,
                "status": 1,
                "sort": 1
            },
            {
                "config_key": "log_dir",
                "config_value": "./Logs",
                "config_type": "string",
                "group_name": "log",
                "description": "日志存储目录",
                "is_system": 1,
                "status": 1,
                "sort": 2
            }
        ]

        tenant_id = 1

        for config_data in default_configs:
            existing = db.query(SystemConfigModel).filter(
                SystemConfigModel.config_key == config_data["config_key"],
                SystemConfigModel.tenant_id == tenant_id,
                SystemConfigModel.is_deleted == 0
            ).first()

            if not existing:
                config = SystemConfigModel(
                    tenant_id=tenant_id,
                    **config_data
                )
                db.add(config)
                print(f"创建配置: {config_data['config_key']}")

        db.commit()
        print("系统配置初始化完成！")

    except Exception as e:
        db.rollback()
        print(f"初始化失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    init_system_configs()
