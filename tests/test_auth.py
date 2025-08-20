import pytest
from fastapi.testclient import TestClient

class TestAuth:
    """测试认证相关接口"""
    
    def test_login_success(self, client: TestClient):
        """测试登录成功"""
        # Use a fixed code that will generate a consistent openid in test mode
        # The MD5 hash of "test_code_fixed" will always be the same
        fixed_code = "test_code_fixed"
        response = client.post(
            "/api/v1/auth/login",
            json={
                "code": fixed_code,
                "userInfo": {
                    "nickName": "测试用户",
                    "avatarUrl": "https://example.com/test.jpg",
                    "gender": 1
                }
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "token" in data["data"]
        assert data["data"]["userInfo"]["nickName"] == "测试用户"
    
    def test_login_with_code_only(self, client: TestClient):
        """测试只使用code登录"""
        response = client.post(
            "/api/v1/auth/login",
            json={"code": "test_code_only"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "token" in data["data"]
    
    def test_login_missing_code(self, client: TestClient):
        """测试缺少code参数"""
        response = client.post(
            "/api/v1/auth/login",
            json={}
        )
        assert response.status_code == 200  # The status code is 200 but the response code is 422
        data = response.json()
        assert data["code"] == 422  # Validation error code