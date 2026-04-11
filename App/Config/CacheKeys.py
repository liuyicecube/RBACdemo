"""Cache Keys Configuration"""

# 权限相关缓存键
USER_PERMISSIONS = "rbac:user:{user_id}:permissions"
ACTIVE_PERMISSIONS = "rbac:permissions:active"

# 菜单相关缓存键
MENU_TREE = "rbac:menu:tree"
USER_MENU_TREE = "rbac:user:{user_id}:menu_tree"

# 用户相关缓存键
ACTIVE_USERS = "rbac:users:active"

# 系统字典相关缓存键
SYSTEM_DICT_ALL = "rbac:dict:all"
SYSTEM_DICT_BY_CODE = "rbac:dict:code:{dict_code}"
SYSTEM_DICT_ITEMS_BY_CODE = "rbac:dict:items:{dict_code}"

# 系统配置相关缓存键
SYSTEM_CONFIG_ALL = "rbac:config:all"
SYSTEM_CONFIG_BY_KEY = "rbac:config:key:{config_key}"

# 用户组相关缓存键
USER_GROUP_ALL = "rbac:user_group:all:tenant:{tenant_id}"
USER_GROUP_BY_ID = "rbac:user_group:id:{group_id}"

# 数据权限规则相关缓存键
DATA_PERMISSION_RULE_ALL = "rbac:data_permission:all:tenant:{tenant_id}"
DATA_PERMISSION_RULE_BY_PERMISSION = "rbac:data_permission:permission:{permission_id}"

# 用户会话相关缓存键
USER_SESSION_BY_ID = "rbac:session:id:{session_id}"
USER_SESSION_BY_USER = "rbac:session:user:{user_id}"
USER_SESSION_ONLINE = "rbac:session:online:tenant:{tenant_id}"

# 用户资料相关缓存键
USER_PROFILE_BY_USER = "rbac:profile:user:{user_id}"

# 缓存过期时间（秒）
CACHE_EXPIRE_5_MINUTES = 300
CACHE_EXPIRE_1_HOUR = 3600
CACHE_EXPIRE_6_HOURS = 21600
CACHE_EXPIRE_12_HOURS = 43200
CACHE_EXPIRE_24_HOURS = 86400
CACHE_EXPIRE_7_DAYS = 604800