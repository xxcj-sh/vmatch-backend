import pytest
from fastapi.testclient import TestClient

class TestProfile:
    """测试个人资料相关接口"""
    
    def test_get_profile_success(self, client: TestClient, auth_headers: dict):
        """测试获取个人资料成功"""
        response = client.get("/api/v1/profile", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["id"] == "user_001"
        assert data["data"]["nickName"] == "小明"
    
    def test_update_profile_success(self, client: TestClient, auth_headers: dict):
        """测试更新个人资料成功"""
        response = client.put(
            "/api/v1/profile",
            json={
                "nickName": "新名字",
                "age": 26,
                "occupation": "高级软件工程师",
                "bio": "更新后的个人简介"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["nickName"] == "新名字"
        assert data["data"]["age"] == 26
        assert data["data"]["occupation"] == "高级软件工程师"
    
    def test_update_profile_partial(self, client: TestClient, auth_headers: dict):
        """测试部分更新个人资料"""
        response = client.put(
            "/api/v1/profile",
            json={
                "bio": "只更新个人简介"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["bio"] == "只更新个人简介"