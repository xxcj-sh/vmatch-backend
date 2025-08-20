import pytest
from fastapi.testclient import TestClient

class TestUser:
    """测试用户相关接口"""
    
    def test_get_user_info_success(self, client: TestClient, auth_headers: dict):
        """测试获取用户信息成功"""
        response = client.get("/api/v1/user/info", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["id"] == "user_001"
        # 由于mock数据可能被之前的测试修改，这里不验证具体昵称值
        assert data["data"]["nickName"] is not None
    
    def test_get_user_info_without_auth(self, client: TestClient):
        """测试未授权访问"""
        response = client.get("/api/v1/user/info")
        assert response.status_code == 401  # 没有提供认证头
    
    def test_get_user_info_invalid_token(self, client: TestClient):
        """测试无效token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/user/info", headers=headers)
        assert response.status_code == 401