#!/usr/bin/env python3
"""
验证 admin 用户权限
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql
import re


def main():
    """主函数"""
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"

    if env_file.exists():
        load_dotenv(env_file)

    database_url = os.getenv("DATABASE_URL", "")

    if not database_url:
        print("错误: 未找到 DATABASE_URL 配置")
        return

    pattern = r"mysql\+pymysql://([^:]+):([^@]+)@([^:/]+):(\d+)/([^?]+)"
    match = re.match(pattern, database_url)

    if not match:
        print("错误: 无法解析数据库 URL")
        return

    db_user = match.group(1)
    db_password = match.group(2)
    db_host = match.group(3)
    db_port = int(match.group(4))
    db_name = match.group(5)

    print("="*60)
    print("验证 admin 用户权限")
    print("="*60)

    conn = pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name,
        charset='utf8mb4'
    )

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, nickname FROM sys_user WHERE username='admin'")
        admin_user = cursor.fetchone()

        if not admin_user:
            print("\n错误: 未找到 admin 用户")
            return

        admin_id = admin_user[0]
        print(f"\n✓ 找到 admin 用户: ID={admin_id}, 用户名={admin_user[1]}, 昵称={admin_user[2]}")

        cursor.execute("""
            SELECT r.id, r.name, r.code
            FROM sys_role r
            INNER JOIN sys_user_role ur ON r.id = ur.role_id
            WHERE ur.user_id = %s
        """, (admin_id,))

        admin_roles = cursor.fetchall()

        print(f"\n✓ admin 用户拥有 {len(admin_roles)} 个角色:")
        for role in admin_roles:
            print(f"  - {role[1]} ({role[2]})")

        cursor.execute("""
            SELECT COUNT(DISTINCT p.id)
            FROM sys_permission p
            INNER JOIN sys_role_permission rp ON p.id = rp.permission_id
            INNER JOIN sys_user_role ur ON rp.role_id = ur.role_id
            WHERE ur.user_id = %s
        """, (admin_id,))

        admin_perm_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sys_permission")
        total_perm_count = cursor.fetchone()[0]

        print(f"\n✓ 权限统计:")
        print(f"  - admin 拥有权限数: {admin_perm_count}")
        print(f"  - 系统总权限数: {total_perm_count}")

        if admin_perm_count == total_perm_count:
            print(f"\n✓✓✓ SUCCESS: admin 用户拥有系统所有 {total_perm_count} 个权限! ✓✓✓")
        else:
            print(f"\n⚠ 警告: admin 用户缺少 {total_perm_count - admin_perm_count} 个权限")

            cursor.execute("""
                SELECT p.id, p.name, p.code
                FROM sys_permission p
                WHERE p.id NOT IN (
                    SELECT DISTINCT p2.id
                    FROM sys_permission p2
                    INNER JOIN sys_role_permission rp ON p2.id = rp.permission_id
                    INNER JOIN sys_user_role ur ON rp.role_id = ur.role_id
                    WHERE ur.user_id = %s
                )
            """, (admin_id,))

            missing_perms = cursor.fetchall()

            if missing_perms:
                print("\n缺少的权限:")
                for perm in missing_perms:
                    print(f"  - {perm[1]} ({perm[2]})")

        print("\n" + "="*60)
        print("验证完成")
        print("="*60 + "\n")

        cursor.close()

    finally:
        conn.close()


if __name__ == "__main__":
    main()
