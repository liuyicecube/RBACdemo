# Enterprise RBAC System 部署文档

## 目录

- [项目简介](#项目简介)
- [技术栈](#技术栈)
- [系统要求](#系统要求)
- [安装步骤](#安装步骤)
- [配置说明](#配置说明)
- [数据库迁移](#数据库迁移)
- [运行项目](#运行项目)
- [部署方式](#部署方式)
- [API文档](#api文档)
- [测试](#测试)
- [常见问题](#常见问题)

---

## 项目简介

Enterprise RBAC System 是一个基于 FastAPI 构建的企业级 RBAC（基于角色的访问控制）系统，提供完整的用户管理、角色管理、权限管理、部门管理、菜单管理等功能。

**主要功能：**

- 用户认证与授权（JWT）
- 用户管理（CRUD、状态管理、角色分配）
- 角色管理（CRUD、权限分配）
- 权限管理（CRUD、批量操作）
- 部门管理（树形结构、用户关联）
- 菜单管理（树形结构、权限关联）
- 系统字典
- 系统配置
- 操作日志
- 审计日志
- 用户组管理
- 数据权限规则
- 用户会话管理

---

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | ^3.10 | 编程语言 |
| FastAPI | ^0.104.0 | Web框架 |
| Uvicorn | ^0.24.0 | ASGI服务器 |
| SQLAlchemy | ^2.0.0 | ORM框架 |
| PyMySQL | ^1.1.0 | MySQL驱动 |
| Alembic | ^1.13.0 | 数据库迁移工具 |
| Pydantic | ^2.5.0 | 数据验证 |
| JWT | ^3.3.0 | 认证令牌 |
| Passlib | ^1.7.4 | 密码哈希 |
| bcrypt | ^4.1.2 | 加密算法 |
| Redis | ^5.0.0 | 缓存/会话 |
| Loguru | ^0.7.2 | 日志 |

---

## 系统要求

### 硬件要求

- CPU: 2核及以上
- 内存: 4GB及以上
- 硬盘: 20GB及以上

### 软件要求

- 操作系统: Windows 10+/Linux/macOS
- Python: 3.10 或更高版本
- MySQL: 8.0 或更高版本（或 MariaDB 10.5+）
- Redis: 6.0 或更高版本（可选，用于缓存）
- Poetry: 1.0 或更高版本（包管理工具）

---

## 安装步骤

### 1. 克隆或下载项目

```bash
# 使用Git克隆
git clone <repository-url>
cd enterprise-rbac-system

# 或者直接下载项目压缩包并解压
```

### 2. 安装Python依赖

#### 方式一：使用Poetry（推荐）

```bash
# 安装Poetry（如果未安装）
# Windows
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# 安装项目依赖
poetry install

# 激活虚拟环境
poetry shell
```

#### 方式二：使用pip

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

> 注意：如果没有requirements.txt，可以使用 `poetry export -f requirements.txt --output requirements.txt` 生成。

### 3. 安装MySQL数据库

#### Windows

下载并安装 MySQL Community Server: https://dev.mysql.com/downloads/mysql/

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### macOS

```bash
brew install mysql
brew services start mysql
```

### 4. 安装Redis（可选）

#### Windows

下载Redis for Windows 或使用 Docker

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

#### macOS

```bash
brew install redis
brew services start redis
```

---

## 配置说明

### 1. 环境变量配置

复制环境变量示例文件：

```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

编辑 `.env` 文件，根据实际情况修改配置：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name?charset=utf8mb4

# JWT配置
JWT_SECRET_KEY=your_secure_random_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis配置（可选）
REDIS_URL=redis://127.0.0.1:6379/0

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

# CORS配置
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=./Logs
```

### 2. 生成JWT密钥

可以使用以下Python代码生成安全的随机密钥：

```python
import secrets
print(secrets.token_hex(32))
```

将生成的密钥填入 `.env` 文件的 `JWT_SECRET_KEY`。

### 3. 创建数据库

```sql
-- 登录MySQL
mysql -u root -p

-- 创建数据库
CREATE DATABASE lydata CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户并授权（可选）
CREATE USER 'rbac_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON lydata.* TO 'rbac_user'@'localhost';
FLUSH PRIVILEGES;

EXIT;
```

---

## 数据库迁移

### 方式一：使用Alembic（推荐）

```bash
# 初始化迁移（如果项目已有迁移脚本，跳过此步）
alembic init alembic

# 创建迁移脚本
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 方式二：使用SQLAlchemy自动创建表

**注意：** 项目默认已禁用自动创建表，建议使用迁移脚本。

如果需要快速测试，可以临时启用：

编辑 `App/Main.py`，取消注释：

```python
Base.metadata.create_all(bind=engine)
```

### 导入演示数据（可选）

如果项目提供了演示数据导入脚本：

```bash
python ImportDemoData.py
```

---

## 运行项目

### 开发模式

```bash
# 使用Poetry
poetry run python -m App.Main

# 或使用uvicorn直接运行
uvicorn App.Main:app --reload --host 0.0.0.0 --port 8000
```

### 生产模式

```bash
# 使用uvicorn（单进程）
uvicorn App.Main:app --host 0.0.0.0 --port 8000 --workers 4

# 或使用Gunicorn + Uvicorn Workers（Linux/macOS）
gunicorn App.Main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 验证服务

启动后，访问以下地址验证服务是否正常：

- **健康检查**: http://localhost:8000/health
- **API文档 (Swagger)**: http://localhost:8000/docs
- **API文档 (ReDoc)**: http://localhost:8000/redoc

---

## 部署方式

### 方式一：使用Docker（推荐）

#### 1. 创建Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 安装Poetry
RUN pip install --no-cache-dir poetry

# 复制项目文件
COPY pyproject.toml poetry.lock ./

# 安装依赖
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# 复制应用代码
COPY App ./App
COPY .env ./

# 创建必要的目录
RUN mkdir -p uploads Logs

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "App.Main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### 2. 创建docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://root:password@mysql:3306/lydata?charset=utf8mb4
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mysql
      - redis
    volumes:
      - ./uploads:/app/uploads
      - ./Logs:/app/Logs
    restart: unless-stopped

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: lydata
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  mysql_data:
  redis_data:
```

#### 3. 启动服务

```bash
docker-compose up -d

# 查看日志
docker-compose logs -f app
```

### 方式二：使用Nginx反向代理

#### 1. 安装Nginx

```bash
# Ubuntu/Debian
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

#### 2. 配置Nginx

创建配置文件 `/etc/nginx/sites-available/rbac-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
    }

    location /redoc {
        proxy_pass http://127.0.0.1:8000/redoc;
        proxy_set_header Host $host;
    }

    access_log /var/log/nginx/rbac-api-access.log;
    error_log /var/log/nginx/rbac-api-error.log;
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/rbac-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 3. 使用systemd管理服务

创建服务文件 `/etc/systemd/system/rbac-api.service`:

```ini
[Unit]
Description=Enterprise RBAC API Service
After=network.target mysql.service redis.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/enterprise-rbac-system
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn App.Main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable rbac-api
sudo systemctl start rbac-api
sudo systemctl status rbac-api
```

### 方式三：使用Supervisor管理进程

```bash
# 安装Supervisor
sudo apt install supervisor

# 创建配置文件 /etc/supervisor/conf.d/rbac-api.conf
[program:rbac-api]
command=/path/to/venv/bin/uvicorn App.Main:app --host 127.0.0.1 --port 8000 --workers 4
directory=/path/to/enterprise-rbac-system
user=www-data
autostart=true
autorestart=true
stdout_logfile=/var/log/rbac-api/stdout.log
stderr_logfile=/var/log/rbac-api/stderr.log
```

---

## API文档

启动服务后，可以通过以下方式访问API文档：

### Swagger UI (交互式文档)

http://localhost:8000/docs

- 支持在线测试API
- 自动生成请求示例
- 显示响应模型

### ReDoc (美观的文档)

http://localhost:8000/redoc

- 三栏布局
- 更好的阅读体验
- 适合打印

### OpenAPI JSON规范

http://localhost:8000/openapi.json

可以导入到Postman、Insomnia等工具中使用。

---

## 测试

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_auth.py

# 运行测试并显示详细信息
python -m pytest -v

# 运行测试并生成覆盖率报告
python -m pytest --cov=App --cov-report=html
```

### 测试覆盖率

项目提供了测试覆盖率检查脚本：

```bash
# 检查覆盖率
python check_coverage.py

# 分析覆盖率报告
python analyze_coverage.py
```

---

## 常见问题

### 1. 数据库连接失败

**错误信息**: `sqlalchemy.exc.OperationalError`

**解决方案**:
- 检查MySQL服务是否启动
- 确认 `.env` 中的数据库连接信息正确
- 检查防火墙是否允许3306端口
- 确认数据库用户有足够权限

### 2. bcrypt/passlib版本兼容性问题

**错误信息**: `AttributeError: module 'bcrypt' has no attribute '__about__'`

**解决方案**:
```bash
poetry add bcrypt==4.0.1
# 或
pip install bcrypt==4.0.1
```

### 3. JWT认证失败

**错误信息**: `401 Unauthorized`

**解决方案**:
- 确认 `JWT_SECRET_KEY` 已正确配置
- 检查token是否过期
- 确认请求头格式正确: `Authorization: Bearer <token>`

### 4. Redis连接失败

**错误信息**: `redis.exceptions.ConnectionError`

**解决方案**:
- 检查Redis服务是否启动
- 确认 `REDIS_URL` 配置正确
- 如果不需要Redis，可以修改代码不使用缓存功能

### 5. 上传文件失败

**错误信息**: 文件上传失败或大小限制

**解决方案**:
- 检查 `UPLOAD_DIR` 目录是否存在且有写权限
- 确认 `MAX_FILE_SIZE` 配置足够大
- 检查Nginx配置中的 `client_max_body_size`

### 6. 性能问题

**优化建议**:
- 使用Gunicorn + Uvicorn多进程模式
- 启用Redis缓存
- 数据库连接池配置优化
- 使用CDN加速静态资源
- 配置日志级别为WARNING或ERROR

---

## 目录结构

```
enterprise-rbac-system/
├── App/                          # 应用主目录
│   ├── Api/                      # API层
│   │   └── V1/                   # API v1版本
│   ├── Config/                   # 配置文件
│   ├── Core/                     # 核心组件
│   ├── Dependencies/             # 依赖注入
│   ├── Models/                   # 数据模型
│   ├── Repositories/             # 数据仓库
│   ├── Schemas/                  # Pydantic模式
│   ├── Services/                 # 业务逻辑层
│   ├── Utils/                    # 工具函数
│   └── Main.py                   # 应用入口
├── Tests/                        # 测试文件
├── alembic/                      # 数据库迁移
├── uploads/                      # 上传文件目录
├── Logs/                         # 日志目录
├── .env                          # 环境变量（不提交到Git）
├── .env.example                  # 环境变量示例
├── PyProject.toml                # Poetry配置
├── pyproject.toml                # 项目配置
├── README.md                     # 本文档
└── ImportDemoData.py             # 演示数据导入
```

---

## 维护与监控

### 日志管理

日志文件存储在 `Logs/` 目录下：
- `app.log` - 应用日志
- `error.log` - 错误日志
- `access.log` - 访问日志

可以使用Logrotate进行日志轮转。

### 数据库备份

```bash
# 备份数据库
mysqldump -u root -p lydata > backup_$(date +%Y%m%d).sql

# 恢复数据库
mysql -u root -p lydata < backup_20240101.sql
```

### 健康检查

定期检查服务状态：

```bash
# 检查服务是否响应
curl http://localhost:8000/health

# 检查进程状态
ps aux | grep uvicorn
```

---

## 安全建议

1. **生产环境必须修改以下配置**:
   - 修改 `JWT_SECRET_KEY` 为强随机密钥
   - 修改数据库密码
   - 设置 `APP_DEBUG=False`
   - 配置HTTPS

2. **防火墙配置**:
   - 仅开放必要端口（80, 443）
   - 限制数据库和Redis访问IP

3. **定期更新依赖**:
   ```bash
   poetry update
   # 或
   pip list --outdated
   ```

4. **定期备份数据库**

5. **监控异常登录和操作日志**

---

## 技术支持

如有问题，请：
1. 查看本文档的常见问题部分
2. 检查日志文件
3. 查看GitHub Issues（如有）

---

## 许可证

[MIT]

---

**最后更新**: 2026-04-12
