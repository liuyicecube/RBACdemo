"""Logger Utils"""

import os
import traceback
from typing import Optional

# 导入loguru的logger，但不直接使用，而是通过LoggerUtils.setup_logger()来配置和获取
from loguru import logger as loguru_logger

from App.Config.Settings import settings


class LoggerUtils:
    """日志工具类"""

    @staticmethod
    def setup_logger():
        """设置日志配置"""
        # 创建日志目录
        os.makedirs(settings.log_dir, exist_ok=True)

        # 移除默认处理器
        loguru_logger.remove()

        # 定义通用格式字符串，使用安全的方式访问extra字典
        def format_record(record):
            """格式化记录，处理缺失的键"""
            extra = record["extra"]

            # 确保所有必要的键存在
            record["extra_request_id"] = extra.get("request_id", "-")
            record["extra_user_id"] = extra.get("user_id", "-")
            record["extra_endpoint"] = extra.get("endpoint", "-")
            record["extra_method"] = extra.get("method", "-")
            record["extra_status_code"] = extra.get("status_code", "-")
            record["extra_response_time"] = extra.get("response_time", "-")
            record["extra_request_size"] = extra.get("request_size", "-")
            record["extra_response_size"] = extra.get("response_size", "-")

            return record

        # 添加控制台处理器
        loguru_logger.add(
            sink=lambda msg: print(msg, end=""),
            level=settings.log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <magenta>{extra_request_id}</magenta> | <yellow>{extra_user_id}</yellow> - <level>{message}</level>",
            colorize=True,
            filter=format_record
        )

        # 添加文件处理器
        loguru_logger.add(
            sink=os.path.join(settings.log_dir, "app.log"),
            level=settings.log_level,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {extra_request_id} | {extra_user_id} - {message}",
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            filter=format_record
        )

        # 添加错误日志处理器
        loguru_logger.add(
            sink=os.path.join(settings.log_dir, "error.log"),
            level="ERROR",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {extra_request_id} | {extra_user_id} - {message}\n{exception}",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            filter=format_record
        )

        # 添加性能日志处理器
        loguru_logger.add(
            sink=os.path.join(settings.log_dir, "performance.log"),
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra_request_id} | {extra_user_id} | {extra_endpoint} | {extra_method} | {extra_status_code} | {extra_response_time}ms | {extra_request_size}B | {extra_response_size}B",
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            filter=format_record
        )

        return loguru_logger

    @staticmethod
    def log_performance(
        request_id: str,
        user_id: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time: float,
        request_size: int = 0,
        response_size: int = 0
    ):
        """记录性能日志"""
        # 确保所有必要字段存在
        extra = {
            "request_id": request_id,
            "user_id": user_id,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_time": round(response_time * 1000, 2),
            "request_size": request_size,
            "response_size": response_size
        }

        loguru_logger.info(
            "Performance log",
            **extra
        )

    @staticmethod
    def log_error(
        message: str,
        request_id: str = "-",
        user_id: str = "-",
        exception: Optional[Exception] = None
    ):
        """记录错误日志"""
        if exception:
            loguru_logger.error(
                message,
                request_id=request_id,
                user_id=user_id,
                exception=traceback.format_exc()
            )
        else:
            loguru_logger.error(
                message,
                request_id=request_id,
                user_id=user_id
            )

    @staticmethod
    def log_warning(
        message: str,
        request_id: str = "-",
        user_id: str = "-"
    ):
        """记录警告日志"""
        loguru_logger.warning(
            message,
            request_id=request_id,
            user_id=user_id
        )

    @staticmethod
    def log_info(
        message: str,
        request_id: str = "-",
        user_id: str = "-"
    ):
        """记录信息日志"""
        loguru_logger.info(
            message,
            request_id=request_id,
            user_id=user_id
        )


# 创建全局日志实例
logger = LoggerUtils.setup_logger()
