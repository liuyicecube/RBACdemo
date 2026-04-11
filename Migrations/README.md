# 数据库迁移脚本

企业级RBAC系统 - 数据库迁移和演示数据导入脚本

## 📁 文件列表

| 文件名 | 说明 |
|--------|------|
| `001_initial_schema.sql` | 数据库表结构（25张表） |
| `002_demo_data.sql` | 演示数据导入脚本 |
| `migrate.py` | 迁移管理工具 |
| `README.md` | 本文档 |

## 🚀 快速开始

### 方法1: 使用迁移管理工具（推荐）

```bash
# 进入Migrations目录
cd Migrations

# 初始化数据库（执行所有迁移）
python migrate.py init

# 重置数据库（删除所有表后重新初始化）
python migrate.py reset

# 列出所有迁移文件
python migrate.py list

# 执行指定的SQL文件
python migrate.py run 001_initial_schema.sql
```

### 方法2: 直接执行SQL文件

```bash
# MySQL
mysql -u username -p database_name < 001_initial_schema.sql
mysql -u username -p database_name < 002_demo_data.sql
```

## 📊 数据库表结构

### 1. 核心基础表（6张）

| 表名 | 说明 |
|------|------|
| `sys_user` | 用户表 |
| `sys_user_profile` | 用户档案表 |
| `sys_role` | 角色表 |
| `sys_permission` | 权限表 |
| `sys_dept` | 部门表 |
| `sys_menu` | 菜单表 |

### 2. 关联表（3张）

| 表名 | 说明 |
|------|------|
| `sys_user_role` | 用户角色关联表 |
| `sys_role_permission` | 角色权限关联表 |
| `sys_menu_permission` | 菜单权限关联表 |

### 3. 用户组相关表（3张）

| 表名 | 说明 |
|------|------|
| `sys_user_group` | 用户组表 |
| `sys_user_group_relation` | 用户-用户组关联表 |
| `sys_user_group_role_relation` | 用户组-角色关联表 |

### 4. 系统配置表（3张）

| 表名 | 说明 |
|------|------|
| `sys_dict` | 系统字典表 |
| `sys_dict_item` | 系统字典项表 |
| `sys_config` | 系统配置表 |

### 5. 日志审计表（3张）

| 表名 | 说明 |
|------|------|
| `sys_operation_log` | 操作日志表 |
| `sys_audit_log` | 审计日志表 |
| `sys_user_session` | 用户会话表 |

### 6. 数据权限表（1张）

| 表名 | 说明 |
|------|------|
| `sys_data_permission_rule` | 数据权限规则表 |

### 7. 系统扩展表（4张）

| 表名 | 说明 |
|------|------|
| `sys_tenant` | 租户表 |
| `sys_notice` | 系统公告表 |
| `sys_file` | 文件表 |
| `sys_migration` | 迁移记录表 |

**总计: 25张表**

## 🎯 演示数据说明

### 默认账号

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| `admin` | `admin123` | 超级管理员 | 拥有所有权限 |
| `zhangsan` | `admin123` | 技术总监 | 技术部门负责人 |
| `lisi` | `admin123` | 部门经理 | 市场部门负责人 |
| `wangwu` | `admin123` | 前端开发 | 前端开发工程师 |
| `zhaoliu` | `admin123` | 后端开发 | 后端开发工程师 |
| `qianqi` | `admin123` | 测试工程师 | 质量测试工程师 |
| `sunba` | `admin123` | 前端开发 | 中级前端工程师 |
| `zhoujiu` | `admin123` | 后端开发 | 中级后端工程师 |
| `wushi` | `admin123` | 普通员工 | 销售经理 |
| `zhengyi` | `admin123` | 普通员工 | 销售专员 |

### 演示数据包含

- ✅ 1个租户
- ✅ 10个系统字典 + 31个字典项
- ✅ 20个系统配置
- ✅ 14个部门（树形结构，4级）
- ✅ 20个菜单（树形结构，3级）
- ✅ 47个权限（树形结构）
- ✅ 8个角色
- ✅ 7个用户组
- ✅ 10个用户（含详细档案）
- ✅ 完整的用户-角色、角色-权限关联
- ✅ 完整的用户组关联
- ✅ 4条系统公告

## 📝 使用示例

### 1. 初始化全新数据库

```bash
cd Migrations
python migrate.py init
```

### 2. 重置数据库（谨慎操作）

```bash
cd Migrations
python migrate.py reset
```

### 3. 仅导入表结构

```bash
python migrate.py run 001_initial_schema.sql
```

### 4. 仅导入演示数据

```bash
python migrate.py run 002_demo_data.sql
```

## 🔧 自定义说明

### 修改密码哈希

演示数据中的密码使用 BCrypt 哈希，如需修改：

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("your_password")
```

### 添加新迁移

1. 在Migrations目录创建新的SQL文件，如 `003_add_new_table.sql`
2. 文件命名格式：`序号_描述.sql`
3. 使用 `migrate.py run` 执行

## 📌 注意事项

1. **备份数据**: 执行reset前请务必备份数据
2. **字符集**: 确保数据库使用 utf8mb4 字符集
3. **外键约束**: 脚本已处理外键约束，按顺序执行
4. **生产环境**: 生产环境请谨慎使用演示数据

## 🔧 故障排除

### 问题1: ImportError: cannot import name 'engine'

**解决**: migrate.py 现在使用原生 pymysql 而不是 SQLAlchemy，无需导入 engine。

### 问题2: AttributeError: 'Settings' object has no attribute 'DATABASE_URL'

**解决**: 已修复，使用小写属性名 `database_url`。

### 问题3: 外键约束错误 (Referencing column ... incompatible)

**解决**: migrate.py 已重写，使用原生 pymysql 直接执行 SQL，避免 SQLAlchemy 自动添加外键约束的问题。

### 问题4: 数据库连接失败

**解决**: 检查 `.env` 文件或 `App/Config/Settings.py` 中的 `database_url` 配置是否正确。

### 问题5: MySQL 驱动未安装

**解决**: 安装 pymysql:
```bash
pip install pymysql
```

## ⚙️ 技术说明

### migrate.py 重写说明

v2.0 版本的 migrate.py 进行了以下改进：

1. **使用原生 pymysql**：不再依赖 SQLAlchemy，直接使用 pymysql 执行 SQL
2. **避免外键约束问题**：SQLAlchemy 会自动解析表关系并添加外键约束，使用原生 pymysql 可以完全避免这个问题
3. **自动创建数据库**：在初始化时会自动检查并创建数据库（如果不存在）
4. **更好的错误处理**：改进了错误提示和连接管理

### 依赖项

- pymysql（必须安装）
