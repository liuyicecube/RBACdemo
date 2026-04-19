"""FastAPI Application Entry"""

from fastapi import FastAPI, Request
from fastapi.security import HTTPBearer
from App.Config.Settings import settings
from App.Core.Middleware import MiddlewareCore
from App.Core.Exceptions import CustomException
from App.Api.Routers import api_router
from App.Utils.Logger import logger


# 注意：不再使用 SQLAlchemy 自动创建表
# 我们通过迁移脚本手动管理数据库结构
# Base.metadata.create_all(bind=engine)

# 定义lifespan上下文管理器
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动事件
    from App.Utils.CacheWarmup import warmup_cache
    warmup_cache()

    yield

    # 关闭事件
    pass

# 创建Bearer认证方案
bearer_scheme = HTTPBearer()

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="企业级RBAC系统API文档",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# 保存原始的openapi方法
original_openapi = app.openapi

# 重写openapi方法，直接修改OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # 获取默认的OpenAPI schema，使用原始方法
    openapi_schema = original_openapi()

    # 添加Bearer认证方案
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # 为所有路径添加安全要求
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "security" not in method:
                method["security"] = [{"BearerAuth": []}]

    # 全局安全要求
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# 设置自定义的openapi方法
app.openapi = custom_openapi

# 添加CORS中间件
MiddlewareCore.add_cors_middleware(app)

# 添加安全头中间件
MiddlewareCore.add_security_headers_middleware(app)

# 添加认证中间件
app.middleware("http")(MiddlewareCore.authentication_middleware)

# 添加日志中间件
app.middleware("http")(MiddlewareCore.logging_middleware)

# 注册API路由
app.include_router(api_router)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    """自定义异常处理"""
    logger.error(f"Custom Exception: {exc.detail}, Code: {exc.error_code}")
    from App.Utils.Response import ResponseUtils
    return ResponseUtils.error(
        message=exc.detail,
        code=exc.status_code,
        error_code=exc.error_code
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    import traceback
    error_detail = traceback.format_exc()
    logger.error(f"Global Exception: {str(exc)}")
    logger.error(f"Exception Detail: {error_detail}")
    from App.Utils.Response import ResponseUtils
    return ResponseUtils.error(
        message=f"服务器内部错误: {str(exc)}",
        code=500,
        error_code=50000
    )


@app.get("/")
def root():
    """根路径"""
    from App.Utils.Response import ResponseUtils
    return ResponseUtils.success(data={
        "app_name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "message": "企业级RBAC系统API服务正在运行中"
    }, message="服务运行正常")


@app.get("/health")
def health_check():
    """健康检查"""
    from App.Utils.Response import ResponseUtils
    return ResponseUtils.success(data={
        "status": "healthy",
        "timestamp": "2023-12-01T12:00:00Z"
    }, message="健康检查通过")


if __name__ == "__main__":
    """应用入口"""
    import uvicorn
    uvicorn.run(
        "App.Main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.app_debug,
        log_level=settings.log_level.lower()
    )
