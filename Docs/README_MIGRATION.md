# 数据库迁移工具使用说明

## 概述

本目录包含数据库迁移相关的脚本和文档，可以帮助您快速初始化数据库表结构和导入演示数据。

## 文件说明

| 文件                   | 说明                    |
| -------------------- | --------------------- |
| `migrate.py`         | Python 迁移脚本（推荐使用）     |
| `migrate.bat`        | Windows 批处理脚本（双击即可运行） |
| `init_schema.sql`    | 数据库表结构初始化脚本           |
| `DATABASE_SCHEMA.md` | 详细的数据库结构文档            |

## 前置要求

- Python 3.8+
- MySQL 5.7+ 或 MySQL 8.0+
- 已安装项目依赖（或至少安装以下库）

### 安装依赖

```bash
pip install sqlalchemy pymysql python-dotenv
```

## 快速开始

### 方式一：使用批处理脚本（Windows）

1. 双击 `Scripts/migrate.bat` 文件
2. 等待脚本执行完成

### 方式二：使用 Python 脚本

```bash
# 进入项目根目录
cd d:\pythonwebapi\enterprise-rbac-system

# 完整迁移（表结构 + 演示数据）
python Scripts\migrate.py

# 仅迁移表结构
python Scripts\migrate.py --schema-only

# 仅导入演示数据
python Scripts\migrate.py --data-only
```

## 配置说明

脚本会自动读取项目根目录下的 `.env` 文件中的 `DATABASE_URL` 配置。

如果没有 `.env` 文件，请先复制 `.env.example` 并重命名为 `.env`，然后修改数据库连接信息：

```env
DATABASE_URL=mysql+pymysql://用户名:密码@主机:端口/数据库名?charset=utf8mb4
```

示例：

```env
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/rbac_system?charset=utf8mb4
```

## 使用示例

### 1. 完整迁移

执行表结构初始化和演示数据导入：

```bash
python Scripts\migrate.py
```

输出示例：

```
============================================================
企业级RBAC系统 - 数据库迁移工具
============================================================
已加载环境配置文件: d:\pythonwebapi\enterprise-rbac-system\.env
数据库配置: root@localhost:3306/rbac_system

检查数据库 'rbac_system' 是否存在...
✓ 数据库 'rbac_system' 已就绪

============================================================
步骤 1/2: 初始化数据库表结构
============================================================

============================================================
开始执行: 数据库表结构初始化
文件: d:\pythonwebapi\enterprise-rbac-system\Scripts\init_schema.sql
============================================================

  进度: 10/100 语句已执行
  进度: 20/100 语句已执行
  ...
  进度: 100/100 语句已执行

✓ 数据库表结构初始化 执行成功!

============================================================
步骤 2/2: 导入演示数据
============================================================

============================================================
开始执行: 演示数据导入
文件: d:\pythonwebapi\enterprise-rbac-system\Migrations\demo_data.sql
============================================================

  进度: 10/50 语句已执行
  ...
  进度: 50/50 语句已执行

✓ 演示数据导入 执行成功!

============================================================
验证迁移结果
============================================================

✓ 数据库中共有 19 张表:
  1. sys_audit_log
  2. sys_config
  3. sys_data_permission_rule
  4. sys_dept
  ...

✓ 用户表中有 10 条记录
✓ 角色表中有 10 条记录
✓ 权限表中有 48 条记录

============================================================
数据库迁移完成!
============================================================

默认登录账号:
  用户名: admin
  密码:   123456

其他测试账号密码均为: 123456
============================================================
```

### 2. 仅迁移表结构

如果只需要创建表结构，不需要演示数据：

```bash
python Scripts\migrate.py --schema-only
```

### 3. 仅导入演示数据

如果表结构已经存在，只需要导入演示数据：

```bash
python Scripts\migrate.py --data-only
```

## 默认账号信息

迁移完成后，可以使用以下账号登录系统：

| 用户名      | 密码        | 角色      | 说明       |
| -------- | --------- | ------- | -------- |
| admin    | admin123! | 超级管理员   | 拥有所有权限   |
| zhangsan | admin123! | 系统管理员   | 技术部负责人   |
| lisi     | admin123! | 系统管理员   | 产品部负责人   |
| wangwu   | admin123! | 部门经理    | 运营部负责人   |
| zhaoliu  | admin123! | 部门经理    | 人力资源部负责人 |
| qianqi   | admin123! | 前端开发工程师 | 前端组长     |
| sunba    | admin123! | 后端开发工程师 | 后端组长     |
| zhoujiu  | admin123! | 测试工程师   | 测试组长     |
| wushi    | admin123! | 前端开发工程师 | 高级前端工程师  |
| zhengyi  | 123456    | 后端开发工程师 | 已离职（禁用）  |

**注意**: 所有测试账号的密码均为 `123456`

## 常见问题

### Q: 提示缺少依赖库怎么办？

A: 安装所需依赖：

```bash
pip install sqlalchemy pymysql python-dotenv
```

### Q: 连接数据库失败怎么办？

A: 检查以下几点：

1. MySQL 服务是否已启动
2. `.env` 文件中的数据库连接信息是否正确
3. 数据库用户是否有足够的权限
4. 防火墙是否允许连接

### Q: 如何只重新导入演示数据？

A: 使用 `--data-only` 参数：

```bash
python Scripts\migrate.py --data-only
```

### Q: 脚本执行一半出错怎么办？

A: 脚本支持断点续传，可以重新运行。如果需要完全重置，可以：

1. 删除数据库
2. 重新创建数据库
3. 再次运行迁移脚本

### Q: 如何自定义数据库名称？

A: 修改 `.env` 文件中的 `DATABASE_URL`，将其中的数据库名改为你想要的名称。脚本会自动创建该数据库（如果不存在）。

## 高级用法

### 使用自定义 SQL 文件

如果需要使用自定义的 SQL 文件，可以直接修改 `migrate.py` 中的文件路径，或者直接使用 MySQL 命令行：

```bash
# 执行自定义 SQL 文件
mysql -u root -p your_database < your_file.sql
```

### 手动执行 SQL

如果 Python 脚本无法满足需求，可以直接使用 MySQL 客户端手动执行：

```bash
# 1. 创建数据库
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS rbac_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. 导入表结构
mysql -u root -p rbac_system < Scripts\init_schema.sql

# 3. 导入演示数据
mysql -u root -p rbac_system < Migrations\demo_data.sql
```

## 相关文档

- `DATABASE_SCHEMA.md` - 详细的数据库结构文档
- `../Migrations/demo_data.sql` - 演示数据脚本
- `../Migrations/OPERATION_GUIDE.md` - 操作指南（如果存在）

## 技术支持

如遇到问题，请检查：

1. Python 版本是否符合要求
2. 数据库连接配置是否正确
3. 错误日志中的具体错误信息

***

**文档版本**: 1.0.0\
**最后更新**: 2026-04-13
