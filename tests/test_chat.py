import pytest
from fastapi.testclient import TestClient

class TestChat:
    """测试聊天相关接口"""
    
    def test_get_chat_history_success(self, client: TestClient, auth_headers: dict):
        """测试获取聊天记录成功"""
        response = client.get(
            "/api/v1/chat/history/match_001?page=1&limit=20",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "total" in data["data"]
        assert "list" in data["data"]
        assert isinstance(data["data"]["list"], list)
    
    def test_get_chat_history_missing_params(self, client: TestClient, auth_headers: dict):
        """测试缺少必要参数"""
        # Since the matchId is now part of the path, we need to test with an invalid path
        # This should be handled by FastAPI's path validation
        response = client.get("/api/v1/chat/history", headers=auth_headers)
        assert response.status_code == 404  # Not Found instead of 422
    
    def test_send_message_success(self, client: TestClient, auth_headers: dict):
        """测试发送消息成功"""
        response = client.post(
            "/api/v1/chat/send",
            json={
                "matchId": "match_001",
                "content": "你好，很高兴认识你！",
                "type": "text"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "id" in data["data"]
        assert "timestamp" in data["data"]
    
    def test_send_message_missing_params(self, client: TestClient, auth_headers: dict):
        """测试发送消息缺少参数"""
        response = client.post(
            "/api/v1/chat/send",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation Error
    
    def test_mark_messages_read_success(self, client: TestClient, auth_headers: dict):
        """测试标记消息已读成功"""
        response = client.post(
            "/api/v1/chat/read",
            json={
                "matchId": "match_001"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0