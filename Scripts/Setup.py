"""
企业RBAC系统 - 一键初始化脚本
功能：
1. 创建数据库和表结构
2. 导入演示数据
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Scripts.InitDatabase import main as init_database_main
from Scripts.ImportDemoData import main as import_demo_main


def main():
    print("=" * 70)
    print("企业RBAC系统 - 一键初始化")
    print("=" * 70)
    
    try:
        print("\n[1/2] 初始化数据库...")
        init_database_main()
        
        print("\n[2/2] 导入演示数据...")
        import_demo_main()
        
        print("\n" + "=" * 70)
        print("[OK] 系统初始化成功完成！")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n[FAIL] 系统初始化失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
