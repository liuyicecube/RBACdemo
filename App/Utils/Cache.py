"""Cache Utility"""

from typing import Optional, Any, Dict
import redis
from App.Config.Settings import settings

# 尝试导入Redis Cluster和Sentinel支持
try:
    from redis.cluster import RedisCluster
    from redis.sentinel import RedisSentinel
    REDIS_CLUSTER_AVAILABLE = True
    REDIS_SENTINEL_AVAILABLE = True
except ImportError:
    REDIS_CLUSTER_AVAILABLE = False
    REDIS_SENTINEL_AVAILABLE = False


class CacheUtils:
    """缓存工具类"""

    def __init__(self):
        """初始化Redis连接，支持单机、Cluster和Sentinel模式"""
        # 命中率统计
        self.hit_count = 0
        self.miss_count = 0
        # 动态过期时间配置
        self.base_expire = 3600  # 基础过期时间（秒）
        self.min_expire = 300  # 最小过期时间（秒）
        self.max_expire = 86400  # 最大过期时间（秒）
        self.high_hit_threshold = 80.0  # 高命中率阈值（百分比）
        self.low_hit_threshold = 40.0  # 低命中率阈值（百分比）

        # 根据配置选择Redis连接方式
        try:
            # 检查是否为Redis Cluster URL
            if settings.redis_url.startswith("redis://") and "," in settings.redis_url:
                # Redis Cluster模式
                if REDIS_CLUSTER_AVAILABLE:
                    print("使用Redis Cluster模式连接")
                    # 解析Cluster节点
                    cluster_nodes = [node.strip() for node in settings.redis_url.replace("redis://", "").split(",")]
                    cluster_kwargs = {
                        "host": cluster_nodes[0].split(":")[0],
                        "port": int(cluster_nodes[0].split(":")[1].split("/")[0]),
                        "decode_responses": True
                    }
                    self.redis_client = RedisCluster(**cluster_kwargs)
                else:
                    print("Redis Cluster支持不可用，降级为单机模式")
                    self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)

            # 检查是否为Redis Sentinel配置
            elif hasattr(settings, "redis_sentinel_urls") and hasattr(settings, "redis_sentinel_master_name"):
                # Redis Sentinel模式
                if REDIS_SENTINEL_AVAILABLE:
                    print("使用Redis Sentinel模式连接")
                    sentinel_urls = [tuple(url.split(":")) for url in settings.redis_sentinel_urls.split(",")]
                    sentinel = RedisSentinel(
                        sentinel_urls,
                        socket_timeout=0.1,
                        decode_responses=True
                    )
                    self.redis_client = sentinel.master_for(settings.redis_sentinel_master_name)
                else:
                    print("Redis Sentinel支持不可用，降级为单机模式")
                    self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)

            # 单机模式
            else:
                print("使用Redis单机模式连接")
                self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)

        except Exception as e:
            print(f"Redis连接失败: {e}")
            print("降级为单机模式连接")
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        try:
            value = self.redis_client.get(key)
            if value:
                self.hit_count += 1
                return value
            else:
                self.miss_count += 1
                return None
        except Exception as e:
            print(f"获取缓存失败: {e}")
            self.miss_count += 1
            return None

    def _get_dynamic_expire(self, base_expire: int) -> int:
        """根据命中率动态计算过期时间"""
        hit_rate = self.get_hit_rate()

        # 根据命中率调整过期时间
        if hit_rate >= self.high_hit_threshold:
            # 高命中率，延长过期时间（最多延长到max_expire）
            dynamic_expire = min(base_expire * 2, self.max_expire)
        elif hit_rate <= self.low_hit_threshold:
            # 低命中率，缩短过期时间（最少缩短到min_expire）
            dynamic_expire = max(base_expire // 2, self.min_expire)
        else:
            # 正常命中率，使用基础过期时间
            dynamic_expire = base_expire

        return dynamic_expire

    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """设置缓存值，根据命中率动态调整过期时间"""
        try:
            # 获取动态过期时间
            dynamic_expire = self._get_dynamic_expire(expire)
            self.redis_client.set(key, value, ex=dynamic_expire)
            return True
        except Exception as e:
            print(f"设置缓存失败: {e}")
            return False

    def delete(self, key: str) -> bool:
        """删除缓存值"""
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"删除缓存失败: {e}")
            return False

    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        try:
            return self.redis_client.exists(key) > 0
        except Exception as e:
            print(f"检查缓存存在性失败: {e}")
            return False

    def get_json(self, key: str) -> Optional[Dict[str, Any]]:
        """获取JSON格式的缓存值"""
        try:
            import json
            value = self.redis_client.get(key)
            if value:
                self.hit_count += 1
                return json.loads(value)
            else:
                self.miss_count += 1
                return None
        except Exception as e:
            print(f"获取JSON缓存失败: {e}")
            self.miss_count += 1
            return None

    def set_json(self, key: str, value: Dict[str, Any], expire: int = 3600) -> bool:
        """设置JSON格式的缓存值，根据命中率动态调整过期时间"""
        try:
            import json
            # 获取动态过期时间
            dynamic_expire = self._get_dynamic_expire(expire)
            self.redis_client.set(key, json.dumps(value), ex=dynamic_expire)
            return True
        except Exception as e:
            print(f"设置JSON缓存失败: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        """删除匹配模式的所有缓存"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"删除匹配缓存失败: {e}")
            return 0

    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """递增缓存值"""
        try:
            return self.redis_client.incr(key, amount)
        except Exception as e:
            print(f"递增缓存失败: {e}")
            return None

    def decr(self, key: str, amount: int = 1) -> Optional[int]:
        """递减缓存值"""
        try:
            return self.redis_client.decr(key, amount)
        except Exception as e:
            print(f"递减缓存失败: {e}")
            return None

    def hget(self, name: str, key: str) -> Optional[Any]:
        """获取哈希表中的值"""
        try:
            value = self.redis_client.hget(name, key)
            return value if value else None
        except Exception as e:
            print(f"获取哈希表值失败: {e}")
            return None

    def hset(self, name: str, key: str, value: Any) -> bool:
        """设置哈希表中的值"""
        try:
            self.redis_client.hset(name, key, value)
            return True
        except Exception as e:
            print(f"设置哈希表值失败: {e}")
            return False

    def hgetall(self, name: str) -> Optional[Dict[str, Any]]:
        """获取哈希表中的所有值"""
        try:
            result = self.redis_client.hgetall(name)
            return result if result else None
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


# 创建全局缓存实例
cache = CacheUtils()

