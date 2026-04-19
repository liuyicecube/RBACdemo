"""测试工具类"""
import pytest
from App.Utils.Security import SecurityUtils
from App.Utils.Response import ResponseUtils
from App.Utils.Tree import TreeUtils

class TestSecurityUtils:
    """测试安全工具"""
    
    def test_password_hashing(self):
        """测试密码哈希和验证"""
        password = "testpassword123"
        hashed = SecurityUtils.hash_password(password)
        
        assert hashed != password
        assert SecurityUtils.verify_password(password, hashed) is True
        assert SecurityUtils.verify_password("wrongpassword", hashed) is False
    
    def test_generate_token(self):
        """测试Token生成"""
        data = {"user_id": 1, "username": "testuser"}
        token = SecurityUtils.create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_verify_token(self):
        """测试Token验证"""
        data = {"user_id": 1, "username": "testuser"}
        token = SecurityUtils.create_access_token(data)
        
        payload = SecurityUtils.verify_token(token)
        assert payload is not None
        assert payload["user_id"] == 1
        assert payload["username"] == "testuser"

class TestResponseUtils:
    """测试响应工具"""
    
    def test_success_response(self):
        """测试成功响应"""
        data = {"key": "value"}
        response = ResponseUtils.success(data=data, message="操作成功")
        
        assert response["code"] == 200
        assert response["message"] == "操作成功"
        assert response["data"] == data
    
    def test_error_response(self):
        """测试错误响应"""
        response = ResponseUtils.error(message="操作失败", code=400, error_code=40001)
        
        assert response["code"] == 400
        assert response["message"] == "操作失败"
        assert response["error_code"] == 40001

class TestTreeUtils:
    """测试树工具"""
    
    def test_build_tree(self):
        """测试构建树"""
        flat_data = [
            {"id": 1, "parent_id": None, "name": "Root"},
            {"id": 2, "parent_id": 1, "name": "Child 1"},
            {"id": 3, "parent_id": 1, "name": "Child 2"},
            {"id": 4, "parent_id": 2, "name": "Grandchild 1"},
        ]
        
        tree = TreeUtils.build_tree(flat_data)
        
        assert len(tree) == 1
        assert tree[0]["id"] == 1
        assert len(tree[0]["children"]) == 2
        assert tree[0]["children"][0]["id"] == 2
        assert len(tree[0]["children"][0]["children"]) == 1
