"""Database Core"""

from sqlalchemy.orm import Session
from typing import Generator
from App.Config.Database import SessionLocal


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
            raise e
