import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from App.Main import app
from App.Config.Database import Base
from App.Dependencies.Database import get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        pass


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.rollback()
        transaction.rollback()
        session.close()
        connection.close()


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


class TestData:
    ADMIN_USER = {
        "username": "admin",
        "password": "Admin@123",
        "email": "admin@example.com"
    }
    
    TEST_USER = {
        "username": "testuser",
        "password": "Test@123",
        "email": "test@example.com"
    }
    
    TEST_USER_2 = {
        "username": "testuser2",
        "password": "Test@123",
        "email": "testuser2@example.com"
    }
    
    TEST_ROLE = {
        "name": "测试角色",
        "code": "test_role",
        "description": "测试角色描述"
    }
    
    TEST_PERMISSION = {
        "name": "测试权限",
        "code": "test:permission",
        "type": 1,
        "description": "测试权限描述"
    }
    
    TEST_MENU = {
        "name": "测试菜单",
        "code": "test_menu",
        "type": 1,
        "path": "/test",
        "sort": 1
    }
    
    TEST_DEPARTMENT = {
        "name": "测试部门",
        "code": "test_dept",
        "sort": 1
    }
    
    TEST_USER_GROUP = {
        "name": "测试用户组",
        "code": "test_group",
        "description": "测试用户组描述"
    }
    
    TEST_SYSTEM_CONFIG = {
        "config_key": "test.config",
        "config_value": "test_value",
        "config_type": "string",
        "group_name": "test",
        "description": "测试配置"
    }
    
    TEST_SYSTEM_DICT = {
        "name": "测试字典",
        "code": "test_dict",
        "description": "测试字典描述"
    }


@pytest.fixture(scope="function")
def test_data():
    return TestData()


@pytest.fixture(scope="function")
def authorized_client(client, test_data):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": test_data.TEST_USER["username"],
            "password": test_data.TEST_USER["password"],
            "nickname": "测试用户",
            "email": test_data.TEST_USER["email"],
            "phone": "13800138000"
        }
    )
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": test_data.TEST_USER["username"],
            "password": test_data.TEST_USER["password"]
        }
    )
    
    if login_response.status_code == 200:
        data = login_response.json()
        if "data" in data and "access_token" in data["data"]:
            token = data["data"]["access_token"]
            client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client


@pytest.fixture(scope="function")
def create_test_user(client, test_data):
    def _create_user(user_data=None):
        if user_data is None:
            user_data = test_data.TEST_USER
        
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "username": user_data["username"],
                "password": user_data["password"],
                "nickname": "测试用户",
                "email": user_data["email"],
                "phone": "13800138000"
            }
        )
        return register_response
    return _create_user


@pytest.fixture(scope="function")
def get_auth_token(client, test_data):
    def _get_token(username=None, password=None):
        if username is None:
            username = test_data.TEST_USER["username"]
        if password is None:
            password = test_data.TEST_USER["password"]
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "username": username,
                "password": password
            }
        )
        
        if login_response.status_code == 200:
            data = login_response.json()
            if "data" in data and "access_token" in data["data"]:
                return data["data"]["access_token"]
        return None
    return _get_token
