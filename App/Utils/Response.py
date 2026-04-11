"""Response Utils"""

import datetime
import json
from typing import Any
from fastapi import status
from fastapi.responses import JSONResponse


def custom_json_encoder(obj):
    """自定义JSON编码器，处理datetime等特殊类型"""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    return obj


def serialize_data(data):
    """序列化数据，处理特殊类型"""
    if isinstance(data, list):
        return [serialize_data(item) for item in data]
    if isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    if hasattr(data, '__dict__'):
        result = {}
        for key, value in data.__dict__.items():
            if not key.startswith('_sa_') and not key.startswith('_'):
                result[key] = serialize_data(value)
        return result
    return custom_json_encoder(data)


class ResponseUtils:
    """响应工具类"""
    
    @staticmethod
    def success(data: Any = None, message: str = "操作成功") -> JSONResponse:
        """成功响应"""
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": status.HTTP_200_OK,
                "message": message,
                "data": serialize_data(data),
                "error_code": 0,
                "timestamp": datetime.datetime.now().isoformat()
            }
        )
    
    @staticmethod
    def created(data: Any = None, message: str = "创建成功") -> JSONResponse:
        """创建成功响应"""
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "code": status.HTTP_201_CREATED,
                "message": message,
                "data": serialize_data(data),
                "error_code": 0
            }
        )
    
    @staticmethod
    def updated(data: Any = None, message: str = "更新成功") -> JSONResponse:
        """更新成功响应"""
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": status.HTTP_200_OK,
                "message": message,
                "data": serialize_data(data),
                "error_code": 0
            }
        )
    
    @staticmethod
    def deleted(data: Any = None, message: str = "删除成功") -> JSONResponse:
        """删除成功响应"""
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": status.HTTP_200_OK,
                "message": message,
                "data": serialize_data(data),
                "error_code": 0
            }
        )
    
    @staticmethod
    def bad_request(message: str = "请求参数错误", error_code: int = 40000) -> JSONResponse:
        """请求参数错误响应"""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": status.HTTP_400_BAD_REQUEST,
                "message": message,
                "data": None,
                "error_code": error_code
            }
        )
    
    @staticmethod
    def unauthorized(message: str = "未授权访问", error_code: int = 40100) -> JSONResponse:
        """未授权响应"""
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": message,
                "data": None,
                "error_code": error_code
            }
        )
    
    @staticmethod
    def forbidden(message: str = "禁止访问", error_code: int = 40300) -> JSONResponse:
        """禁止访问响应"""
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "code": status.HTTP_403_FORBIDDEN,
                "message": message,
                "data": None,
                "error_code": error_code
            }
        )
    
    @staticmethod
    def not_found(message: str = "资源不存在", error_code: int = 40400) -> JSONResponse:
        """资源不存在响应"""
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": status.HTTP_404_NOT_FOUND,
                "message": message,
                "data": None,
                "error_code": error_code
            }
        )
    
    @staticmethod
    def internal_server_error(message: str = "服务器内部错误", error_code: int = 50000) -> JSONResponse:
        """服务器内部错误响应"""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": message,
                "data": None,
                "error_code": error_code
            }
        )
    
    @staticmethod
    def conflict(message: str = "资源冲突", error_code: int = 40900) -> JSONResponse:
        """资源冲突响应"""
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": status.HTTP_409_CONFLICT,
                "message": message,
                "data": None,
                "error_code": error_code
            }
        )
    
    @staticmethod
    def validation_error(message: str = "数据验证失败", error_code: int = 42200) -> JSONResponse:
        """数据验证失败响应"""
        # 使用新的状态码常量，避免弃用警告
        try:
            # 尝试使用新的常量名
            status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        except AttributeError:
            # 如果新常量不可用，回退到旧常量
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        
        return JSONResponse(
            status_code=status_code,
            content={
                "code": status_code,
                "message": message,
                "data": None,
                "error_code": error_code
            }
        )
    
    @staticmethod
    def pagination(data: Any, total: int, page: int, page_size: int, message: str = "操作成功") -> JSONResponse:
        """分页响应"""
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": status.HTTP_200_OK,
                "message": message,
                "data": {
                    "items": serialize_data(data),
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "pages": (total + page_size - 1) // page_size
                },
                "error_code": 0
            }
        )
    
    @staticmethod
    def error(message: str = "服务器内部错误", code: int = 500, error_code: int = 50000) -> JSONResponse:
        """错误响应"""
        return JSONResponse(
            status_code=code,
            content={
                "code": code,
                "message": message,
                "data": None,
                "error_code": error_code
            }
        )
