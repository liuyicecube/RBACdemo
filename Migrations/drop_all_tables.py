#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除所有表
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


def main():
    print("=== 删除所有表 ===\n")
    
    db_config = parse_db_url(settings.database_url)
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            print(f"  删除: {table}")
            cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        
        print(f"\n[OK] 删除了 {len(tables)} 个表")
        
    except Exception as e:
        conn.rollback()
        print(f"\n[FAIL] 删除失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
