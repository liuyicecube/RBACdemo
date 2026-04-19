"""Simple Memory Cache - Fallback for when Redis is not available"""

from typing import Optional, Any, Dict
import time
import json


class SimpleCache:
    """简单的内存缓存，用于Redis不可用时的降级方案"""

    def __init__(self):
        """初始化内存缓存"""
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.hit_count = 0
        self.miss_count = 0
        print("使用内存缓存模式（Redis不可用）")

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        try:
            if key not in self.cache:
                self.miss_count += 1
                return None
            
            item = self.cache[key]
            # 检查是否过期
            if item['expire_at'] is not None and time.time() > item['expire_at']:
                del self.cache[key]
                self.miss_count += 1
                return None
            
            self.hit_count += 1
            return item['value']
        except Exception as e:
            print(f"获取缓存失败: {e}")
            self.miss_count += 1
            return None

    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """设置缓存值"""
        try:
            expire_at = time.time() + expire if expire else None
            self.cache[key] = {
                'value': value,
                'expire_at': expire_at
            }
            return True
        except Exception as e:
            print(f"设置缓存失败: {e}")
            return False

    def delete(self, key: str) -> bool:
        """删除缓存值"""
        try:
            if key in self.cache:
                del self.cache[key]
            return True
        except Exception as e:
            print(f"删除缓存失败: {e}")
            return False

    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        try:
            if key not in self.cache:
                return False
            
            item = self.cache[key]
            if item['expire_at'] is not None and time.time() > item['expire_at']:
                del self.cache[key]
                return False
            
            return True
        except Exception as e:
            print(f"检查缓存存在性失败: {e}")
            return False

    def get_json(self, key: str) -> Optional[Dict[str, Any]]:
        """获取JSON格式的缓存值"""
        try:
            value = self.get(key)
            if value and isinstance(value, str):
                return json.loads(value)
            return value
        except Exception as e:
            print(f"获取JSON缓存失败: {e}")
            self.miss_count += 1
            return None

    def set_json(self, key: str, value: Dict[str, Any], expire: int = 3600) -> bool:
        """设置JSON格式的缓存值"""
        try:
            return self.set(key, json.dumps(value), expire)
        except Exception as e:
            print(f"设置JSON缓存失败: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        """删除匹配模式的所有缓存"""
        try:
            import fnmatch
            keys_to_delete = [k for k in self.cache.keys() if fnmatch.fnmatch(k, pattern)]
            for key in keys_to_delete:
                del self.cache[key]
            return len(keys_to_delete)
        except Exception as e:
            print(f"删除匹配缓存失败: {e}")
            return 0

    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """递增缓存值"""
        try:
            if key not in self.cache:
                self.set(key, amount)
                return amount
            
            item = self.cache[key]
            if item['expire_at'] is not None and time.time() > item['expire_at']:
                del self.cache[key]
                self.set(key, amount)
                return amount
            
            new_value = int(item['value']) + amount
            self.set(key, new_value)
            return new_value
        except Exception as e:
            print(f"递增缓存失败: {e}")
            return None

    def decr(self, key: str, amount: int = 1) -> Optional[int]:
        """递减缓存值"""
        try:
            return self.incr(key, -amount)
        except Exception as e:
            print(f"递减缓存失败: {e}")
            return None

    def hget(self, name: str, key: str) -> Optional[Any]:
        """获取哈希表中的值"""
        try:
            hash_data = self.get(name)
            if hash_data and isinstance(hash_data, dict):
                return hash_data.get(key)
            return None
        except Exception as e:
            print(f"获取哈希表值失败: {e}")
            return None

    def hset(self, name: str, key: str, value: Any) -> bool:
        """设置哈希表中的值"""
        try:
            hash_data = self.get(name)
            if not hash_data or not isinstance(hash_data, dict):
                hash_data = {}
            
            hash_data[key] = value
            return self.set(name, hash_data)
        except Exception as e:
            print(f"设置哈希表值失败: {e}")
            return False

    def hgetall(self, name: str) -> Optional[Dict[str, Any]]:
        """获取哈希表中的所有值"""
        try:
            hash_data = self.get(name)
            if hash_data and isinstance(hash_data, dict):
                return hash_data
            return None
        except Exception as e:
            print(f"获取哈希表所有值失败: {e}")
            return None

    def get_hit_rate(self) -> float:
        """获取缓存命中率"""
        total = self.hit_count + self.miss_count
        if total == 0:
            return 0.0
        return round(self.hit_count / total * 100, 2)

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total = self.hit_count + self.miss_count
        return {
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "total_requests": total,
            "hit_rate": self.get_hit_rate()
        }
