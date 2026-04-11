"""
清除所有权限和菜单相关的缓存
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from App.Utils.Cache import cache
from App.Config.CacheKeys import USER_PERMISSIONS, USER_MENU_TREE, MENU_TREE


def clear_cache():
    """清除所有相关缓存"""
    print("正在清除缓存...")
    
    # 清除所有用户权限缓存
    count1 = cache.delete_pattern(USER_PERMISSIONS.format(user_id="*"))
    print(f"[OK] 清除了 {count1} 个用户权限缓存")
    
    # 清除所有用户菜单树缓存
    count2 = cache.delete_pattern(USER_MENU_TREE.format(user_id="*"))
    print(f"[OK] 清除了 {count2} 个用户菜单树缓存")
    
    # 清除菜单树缓存
    cache.delete(MENU_TREE)
    print("[OK] 清除了菜单树缓存")
    
    print("\n[OK] 缓存清除完成！")


if __name__ == "__main__":
    clear_cache()
