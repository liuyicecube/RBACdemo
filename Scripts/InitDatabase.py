"""
企业RBAC系统 - 数据库迁移脚本
功能：
1. 删除并重建数据库
2. 创建所有数据表
3. 确保表结构完整性
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from App.Config.Database import engine, Base, SessionLocal
from App.Config.Settings import settings
from sqlalchemy import text
from sqlalchemy.engine import make_url
import pymysql

from App.Models.User import UserModel
from App.Models.Role import RoleModel
from App.Models.Permission import PermissionModel
from App.Models.Department import DepartmentModel
from App.Models.Menu import MenuModel
from App.Models.UserRole import UserRoleModel
from App.Models.RolePermission import RolePermissionModel
from App.Models.DataPermissionRule import DataPermissionRuleModel
from App.Models.OperationLog import OperationLogModel
from App.Models.UserSession import UserSessionModel
from App.Models.AuditLog import AuditLogModel
from App.Models.SystemDict import SystemDictModel
from App.Models.SystemDictItem import SystemDictItemModel
from App.Models.UserGroup import UserGroupModel
from App.Models.UserGroupRelation import UserGroupRelationModel
from App.Models.UserGroupRoleRelation import UserGroupRoleRelationModel
from App.Models.MenuPermission import MenuPermissionModel
from App.Models.SystemConfig import SystemConfigModel
from App.Models.UserProfile import UserProfileModel


def drop_database():
    """删除数据库"""
    print("正在删除数据库...")
    try:
        url = make_url(settings.database_url)
        db_name = url.database
        host = url.host
        port = url.port or 3306
        user = url.username
        password = url.password or ""
        
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset="utf8mb4"
        )
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`")
        cursor.execute(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[OK] 数据库 {db_name} 已重建")
    except Exception as e:
        print(f"[FAIL] 删除数据库失败: {e}")
        raise


def create_tables():
    """创建所有数据表"""
    print("正在创建数据表...")
    try:
        Base.metadata.create_all(bind=engine)
        print("[OK] 所有数据表创建成功！")
    except Exception as e:
        print(f"[FAIL] 创建数据表失败: {e}")
        raise


def verify_tables():
    """验证表结构"""
    print("\n正在验证表结构...")
    db = SessionLocal()
    try:
        result = db.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        
        print(f"\n已创建的表（共 {len(tables)} 个）:")
        for table_name in tables:
            result = db.execute(text(f"DESCRIBE `{table_name}`"))
            columns = [row[0] for row in result]
            print(f"  - {table_name} ({len(columns)} 个字段)")
        
        return True
    except Exception as e:
        print(f"[FAIL] 验证表结构失败: {e}")
        return False
    finally:
        db.close()


def main():
    print("=" * 70)
    print("企业RBAC系统 - 数据库迁移脚本")
    print("=" * 70)
    
    try:
        drop_database()
        create_tables()
        is_valid = verify_tables()
        
        print("\n" + "=" * 70)
        if is_valid:
            print("[OK] 数据库迁移成功完成！")
        else:
            print("[WARN] 警告: 部分表结构可能有问题")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n[FAIL] 数据库迁移失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
