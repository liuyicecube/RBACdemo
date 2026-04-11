"""Database Dependencies"""

from sqlalchemy.orm import Session
from typing import Generator
from App.Core.Database import DatabaseCore


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话依赖"""
    yield from DatabaseCore.get_db()