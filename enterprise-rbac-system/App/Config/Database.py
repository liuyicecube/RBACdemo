"""Database Configuration"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from App.Config.Settings import settings
import pymysql
import re


# 解析数据库URL，提取数据库名称
def parse_db_url(db_url):
    """解析数据库URL，提取数据库名称"""
    if db_url.startswith("mysql"):
        # 匹配MySQL URL格式
        match = re.match(r"mysql://.*?@.*?/(.*?)(\?|$)", db_url)
        if match:
            return match.group(1)
    return None


# 获取数据库名称
db_name = parse_db_url(settings.database_url)

# 如果是MySQL数据库，尝试创建数据库
if settings.database_url.startswith("mysql") and db_name:
    # 解析数据库连接信息
    import urllib.parse
    parsed_url = urllib.parse.urlparse(settings.database_url)
    db_config = {
        "host": parsed_url.hostname,
        "port": parsed_url.port or 3306,
        "user": parsed_url.username,
        "password": parsed_url.password,
        "charset": "utf8mb4"
    }

    try:
        # 连接到MySQL服务器（不指定数据库）
        connection = pymysql.connect(**db_config)
        connection.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        connection.close()
        print(f"数据库 {db_name} 已创建或已存在")
    except Exception as e:
        print(f"创建数据库 {db_name} 失败: {e}")


# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
