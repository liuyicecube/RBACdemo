#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单脚本：只执行正确的两个 SQL 文件
"""

import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from App.Config.Settings import settings

try:
    import pymysql
except ImportError:
    print("Error: Please install pymysql first")
    sys.exit(1)


def parse_db_url(db_url):
    if db_url.startswith("mysql+pymysql://"):
        db_url = db_url.replace("mysql+pymysql://", "mysql://")
    parsed = urllib.parse.urlparse(db_url)
    config = {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 3306,
        "user": parsed.username or "root",
        "password": parsed.password or "",
        "charset": "utf8mb4"
    }
    if parsed.path and len(parsed.path) > 1:
        config["database"] = parsed.path[1:]
    return config


def execute_sql_file(file_path, conn):
    """执行单个 SQL 文件"""
    print(f"\n正在执行: {file_path.name}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
    
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 简单的分割（处理注释）
        statements = []
        current = []
        in_comment = False
        
        for line in sql_content.split("\n"):
            line = line.strip()
            if not line or line.startswith("--"):
                continue
            if line.startswith("/*"):
                in_comment = True
            if in_comment:
                if "*/" in line:
                    in_comment = False
                continue
            current.append(line)
            if line.endswith(";"):
                statements.append(" ".join(current))
                current = []
        
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    print(f"  [WARN] 警告: {e}")
                    print(f"  语句: {stmt[:100]}...")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        print(f"[OK] 执行成功: {file_path.name}")
        
    except Exception as e:
        conn.rollback()
        print(f"[FAIL] 执行失败: {file_path.name}")
        print(f"  错误: {e}")
        raise
    finally:
        cursor.close()


def main():
    print("=== 数据库初始化 ===")
    
    db_config = parse_db_url(settings.database_url)
    print(f"数据库: {db_config.get('database', '(未指定)')}")
    print()
    
    # 获取 SQL 文件
    migration_dir = Path(__file__).parent
    sql_files = [
        migration_dir / "001_initial_schema.sql",
        migration_dir / "002_demo_data.sql"
    ]
    
    conn = pymysql.connect(**db_config)
    
    try:
        for sql_file in sql_files:
            if sql_file.exists():
                execute_sql_file(sql_file, conn)
        
        print("\n=== 初始化成功 ===")
        
    finally:
        conn.close()


if __name__ == "__main__":
    main()
