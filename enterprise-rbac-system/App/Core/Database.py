"""Database Core"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Generator, Dict, Any
from datetime import datetime
from App.Config.Database import SessionLocal
from App.Utils.Logger import logger


class DatabaseCore:
    """数据库核心功能"""

    @staticmethod
    def get_db() -> Generator[Session, None, None]:
        """获取数据库会话"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def commit_rollback(db: Session) -> None:
        """提交或回滚事务"""
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"数据库事务提交失败: {str(e)}")
            raise e

    @staticmethod
    def health_check() -> Dict[str, Any]:
        """数据库健康检查"""
        start_time = datetime.now()
        try:
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            latency = (datetime.now() - start_time).total_seconds() * 1000
            db.close()
            
            logger.info(f"数据库健康检查成功，延迟: {latency:.2f}ms")
            return {
                "status": "healthy",
                "latency_ms": round(latency, 2),
                "check_time": datetime.now().isoformat()
            }
        except Exception as e:
            latency = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"数据库健康检查失败: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "latency_ms": round(latency, 2),
                "check_time": datetime.now().isoformat()
            }

    @staticmethod
    def get_connection_info() -> Dict[str, Any]:
        """获取数据库连接信息"""
        try:
            db = SessionLocal()
            result = db.execute(text("SELECT version()"))
            version = result.scalar()
            db.close()
            
            return {
                "version": version,
                "check_time": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取数据库连接信息失败: {str(e)}")
            return {
                "error": str(e),
                "check_time": datetime.now().isoformat()
            }
