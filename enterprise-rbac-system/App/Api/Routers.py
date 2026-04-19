"""API Routers Registration"""

from fastapi import APIRouter
from App.Api.V1 import api_v1_router


# 创建主API路由
api_router = APIRouter(prefix="/api")

# 注册V1版本路由
api_router.include_router(api_v1_router)

# 可以在这里添加更多版本的路由，例如V2
# from App.Api.V2 import api_v2_router
# api_router.include_router(api_v2_router)
