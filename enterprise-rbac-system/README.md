# 企业级RBAC系统 - 后端部署文档

## 项目概述

企业级RBAC系统是一个基于FastAPI构建的权限管理系统，提供用户管理、角色管理、权限管理、部门管理等功能。

### 技术栈

- **Web框架**: FastAPI 0.104.0
- **ASGI服务器**: Uvicorn 0.24.0
- **ORM**: SQLAlchemy 2.0.0
- **数据库**: MySQL 8.0+ (使用PyMySQL驱动)
- **缓存**: Redis 5.0.0
- **数据验证**: Pydantic 2.5.0
- **安全认证**: JWT (python-jose) + BCrypt
- **日志**: Loguru 0.7.2

### 系统要求

- Python 3.10 或更高版本
- MySQL 8.0 或更高版本
- Redis 5.0 或更高版本
- 至少 2GB RAM
- 至少 10GB 磁盘空间

---

## 目录结构

```
enterprise-rbac-system/
├── App/
│   ├── Api/
│   │   └── V1/          # API路由
│   ├── Config/         # 配置文件
│   ├── Core/           # 核心组件
│   ├── Dependencies/   # 依赖注入
│   ├── Models/         # 数据模型
│   ├── Repositories/   # 数据访问层
│   ├── Schemas/        # 数据传输对象
│   ├── Services/       # 业务逻辑层
│   ├── Utils/          # 工具函数
│   ├── Main.py         # 应用入口
│   └── __init__.py
├── Logs/               # 日志目录
├── Migrations/         # 迁移脚本
├── Requirements/       # 依赖文件
├── Scripts/            # 初始化脚本
├── Tests/              # 测试文件
├── .env                # 环境变量配置
├── .env.example        # 环境变量示例
├── PyProject.toml      # Poetry配置
└── README.md           # 本文档
```

---

## 部署步骤

### 1. 环境准备

#### 1.1 安装Python 3.10+

从 [Python官网](https://www.python.org/downloads/) 下载并安装Python 3.10或更高版本。

验证安装：

```bash
python --version
```

#### 1.2 安装MySQL 8.0+

从 [MySQL官网](https://dev.mysql.com/downloads/mysql/) 下载并安装MySQL。

创建数据库和用户：

```sql
CREATE DATABASE rbac_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rbac_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON rbac_system.* TO 'rbac_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 1.3 安装Redis

从 [Redis官网](https://redis.io/download) 下载并安装Redis，或使用Docker：

```bash
docker run -d -p 6379:6379 --name rbac-redis redis:5-alpine
```

### 2. 项目安装

#### 2.1 克隆项目

```bash
cd /path/to/your/projects
git clone <repository-url>
cd enterprise-rbac-system
```

#### 2.2 创建虚拟环境（推荐）

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 安装依赖

生产环境：

```bash
pip install -r Requirements/Prod.txt
```

开发环境：

```bash
pip install -r Requirements/Dev.txt
```

或者使用Poetry：

```bash
pip install poetry
poetry install
```

### 3. 配置环境变量

复制示例配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，修改以下配置：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://rbac_user:your_secure_password@localhost:3306/rbac_system?charset=utf8mb4

# JWT配置（请替换为随机生成的密钥）
JWT_SECRET_KEY=your_random_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis配置
REDIS_URL=redis://localhost:6379/0

# 应用配置
APP_NAME=Enterprise RBAC System
APP_VERSION=1.0.0
APP_DEBUG=False

# 安全配置
PASSWORD_SALT_LENGTH=16
BCRYPT_ROUNDS=12

# 上传配置
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
ALLOWED_IMAGE_EXTENSIONS=png,jpg,jpeg,gif

# CORS配置（根据实际情况修改）
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:5175

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=./Logs
```

#### 生成JWT密钥

可以使用Python生成安全的JWT密钥：

```python
import secrets
print(secrets.token_urlsafe(32))
```

### 4. 初始化数据库

#### 4.1 执行初始化脚本

使用MySQL客户端执行初始化脚本：

```bash
mysql -u rbac_user -p rbac_system < Scripts/init_schema.sql
```

或者通过Python执行：

```python
from App.Config.Settings import settings
from App.Core.Database import engine, Base

# 注意：项目使用手动迁移脚本，不建议使用自动创建表
# Base.metadata.create_all(bind=engine)
```

#### 4.2 验证数据库

连接到数据库，确认所有表都已创建：

```sql
USE rbac_system;
SHOW TABLES;
```

应该看到以下19张表：
- sys_user
- sys_user_profile
- sys_role
- sys_user_role
- sys_permission
- sys_role_permission
- sys_dept
- sys_menu
- sys_menu_permission
- sys_user_group
- sys_user_group_relation
- sys_user_group_role_relation
- sys_user_session
- sys_audit_log
- sys_operation_log
- sys_config
- sys_dict
- sys_dict_item
- sys_data_permission_rule

### 5. 创建必要的目录

```bash
mkdir -p Logs
mkdir -p uploads
```

### 6. 运行应用

#### 6.1 开发环境运行

```bash
python App/Main.py
```

或使用Uvicorn：

```bash
uvicorn App.Main:app --reload --host 0.0.0.0 --port 8000
```

#### 6.2 生产环境运行

使用Uvicorn（推荐）：

```bash
uvicorn App.Main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```

使用Gunicorn + Uvicorn workers：

```bash
pip install gunicorn
gunicorn App.Main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --access-logfile - --error-logfile -
```

#### 6.3 使用进程管理器（推荐用于生产）

##### 使用systemd（Linux）

创建服务文件 `/etc/systemd/system/rbac-backend.service`：

```ini
[Unit]
Description=Enterprise RBAC Backend
After=network.target mysql.service redis.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/enterprise-rbac-system
Environment="PATH=/path/to/enterprise-rbac-system/venv/bin"
ExecStart=/path/to/enterprise-rbac-system/venv/bin/uvicorn App.Main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable rbac-backend
sudo systemctl start rbac-backend
sudo systemctl status rbac-backend
```

##### 使用PM2（跨平台）

安装PM2：

```bash
npm install -g pm2
```

创建 `ecosystem.config.js`：

```javascript
module.exports = {
  apps: [{
    name: 'rbac-backend',
    script: 'uvicorn',
    args: 'App.Main:app --host 0.0.0.0 --port 8000 --workers 4',
    interpreter: '/path/to/venv/bin/python',
    cwd: '/path/to/enterprise-rbac-system',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    }
  }]
};
```

启动应用：

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### 7. 配置反向代理（推荐）

#### 7.1 使用Nginx

创建Nginx配置文件 `/etc/nginx/sites-available/rbac-backend`：

```nginx
upstream rbac_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://rbac_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 静态文件（如果有）
    location /uploads/ {
        alias /path/to/enterprise-rbac-system/uploads/;
        expires 30d;
    }
}
```

启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/rbac-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 7.2 使用Caddy

创建 `Caddyfile`：

```
your-domain.com {
    reverse_proxy 127.0.0.1:8000
    
    @uploads path /uploads/*
    handle @uploads {
        root * /path/to/enterprise-rbac-system
        file_server
    }
}
```

启动Caddy：

```bash
caddy run
```

### 8. SSL证书配置（生产环境必须）

#### 使用Let's Encrypt + Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

Certbot会自动配置Nginx并设置证书自动续期。

---

## 验证部署

### 1. 健康检查

访问：
```
http://your-domain.com/health
```

应该返回：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "status": "healthy",
    "timestamp": "2023-12-01T12:00:00Z"
  }
}
```

### 2. API文档

访问Swagger UI文档：
```
http://your-domain.com/docs
```

访问ReDoc文档：
```
http://your-domain.com/redoc
```

### 3. 根路径检查

访问：
```
http://your-domain.com/
```

应该返回系统信息。

---

## 配置说明

### 数据库配置

```env
DATABASE_URL=mysql+pymysql://user:password@host:port/database?charset=utf8mb4
```

参数说明：
- user: 数据库用户名
- password: 数据库密码
- host: 数据库主机地址
- port: 数据库端口（默认3306）
- database: 数据库名称

### JWT配置

```env
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Redis配置

单实例：
```env
REDIS_URL=redis://localhost:6379/0
```

Sentinel模式（可选）：
```env
REDIS_SENTINEL_URLS=redis://sentinel1:26379,redis://sentinel2:26379
REDIS_SENTINEL_MASTER_NAME=mymaster
```

### CORS配置

```env
CORS_ORIGINS=http://localhost:3000,https://your-frontend.com
```

多个域名使用逗号分隔。

---

## 日志管理

日志文件存储在 `Logs/` 目录：
- `app.log`: 应用日志
- `error.log`: 错误日志
- `performance.log`: 性能日志

日志轮转：
- 日志文件会自动轮转
- 保留最近30天的日志
- 单个日志文件最大100MB

---

## 备份与恢复

### 数据库备份

```bash
mysqldump -u rbac_user -p rbac_system > backup_$(date +%Y%m%d).sql
```

### 数据库恢复

```bash
mysql -u rbac_user -p rbac_system < backup_20240101.sql
```

### 文件备份

```bash
tar -czf uploads_$(date +%Y%m%d).tar.gz uploads/
```

---

## 监控与维护

### 常用命令

查看应用状态：
```bash
# systemd
sudo systemctl status rbac-backend

# PM2
pm2 status
```

查看日志：
```bash
# systemd
sudo journalctl -u rbac-backend -f

# PM2
pm2 logs rbac-backend
```

重启应用：
```bash
# systemd
sudo systemctl restart rbac-backend

# PM2
pm2 restart rbac-backend
```

### 性能监控

- 使用 `htop` 监控系统资源
- 使用 `mysqladmin processlist` 监控数据库连接
- 使用 `redis-cli info` 监控Redis状态

---

## 安全建议

1. **环境变量保护**: 确保 `.env` 文件权限正确，不要提交到版本控制
2. **HTTPS**: 生产环境必须使用HTTPS
3. **防火墙**: 只开放必要的端口（80, 443）
4. **数据库安全**: 使用强密码，限制远程访问
5. **定期更新**: 及时更新依赖包和系统补丁
6. **日志审计**: 定期检查日志文件
7. **备份策略**: 建立定期备份机制

---

## 故障排查

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务是否启动
   - 验证数据库连接配置
   - 检查防火墙设置

2. **Redis连接失败**
   - 检查Redis服务是否启动
   - 验证Redis连接配置

3. **权限错误**
   - 确保应用有读写日志和上传目录的权限

4. **端口被占用**
   - 修改配置中的端口号
   - 或停止占用端口的程序

### 日志查看

查看应用日志：
```bash
tail -f Logs/app.log
tail -f Logs/error.log
```

---

## 开发指南

### 运行测试

```bash
pip install pytest pytest-asyncio httpx
python -m pytest Tests/ -v
```

### 代码格式化

```bash
black .
isort .
flake8 .
```

---

## 更新与升级

### 更新依赖

```bash
pip list --outdated
pip install --upgrade -r Requirements/Prod.txt
```

### 数据库迁移

执行迁移脚本：
```bash
mysql -u rbac_user -p rbac_system < Migrations/migration_script.sql
```

---

## 技术支持

如有问题，请查看：
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- 项目Issues页面

---

## 许可证

本项目采用MIT许可证。

---

**最后更新**: 2026-04-19
