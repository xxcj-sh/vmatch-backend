import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any

class TestMatch:
    """测试匹配相关接口"""
    
    def test_get_match_cards_success(self, client: TestClient, auth_headers: Dict[str, Any]):
        """测试获取匹配卡片成功"""
        response = client.get(
            "/api/v1/match/cards?matchType=dating&userRole=seeker&page=1&pageSize=10",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "total" in data["data"]
        assert "list" in data["data"]
        assert isinstance(data["data"]["list"], list)
    
    def test_get_match_cards_missing_params(self, client: TestClient, auth_headers: Dict[str, Any]):
        """测试缺少必要参数"""
        response = client.get("/api/v1/match/cards", headers=auth_headers)
        assert response.status_code == 422
    
    def test_submit_match_action_like(self, client: TestClient, auth_headers: Dict[str, Any]):
        """测试点赞操作"""
        response = client.post(
            "/api/v1/match/action",
            json={
                "cardId": "card_001",
                "action": "like",
                "matchType": "dating"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "isMatch" in data["data"]
        assert "matchId" in data["data"]
    
    def test_submit_match_action_dislike(self, client: TestClient, auth_headers: Dict[str, Any]):
        """测试不喜欢操作"""
        response = client.post(
            "/api/v1/match/action",
            json={
                "cardId": "card_002",
                "action": "dislike",
                "matchType": "dating"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["isMatch"] is False
        assert data["data"]["matchId"] is None
    
    def test_get_match_list_success(self, client: TestClient, auth_headers: Dict[str, Any]):
        """测试获取匹配列表成功"""
        response = client.get("/api/v1/match/list?status=all&page=1&pageSize=10", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "total" in data["data"]
        assert "list" in data["data"]
        assert isinstance(data["data"]["list"], list)
    
    def test_swipe_card_right(self, client: TestClient, auth_headers: Dict[str, Any]):
        """测试右滑卡片（喜欢）"""
        response = client.post(
            "/api/v1/match/swipe",
            json={
                "cardId": "card_001",
                "direction": "right"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "isMatch" in data["data"]
    
    def test_swipe_card_left(self, client: TestClient, auth_headers: Dict[str, Any]):
        """测试左滑卡片（不喜欢）"""
        response = client.post(
            "/api/v1/match/swipe",
            json={
                "cardId": "card_002",
                "direction": "left"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["isMatch"] is False
    
    def test_swipe_card_up(self, client: TestClient, auth_headers: Dict[str, Any]):
        """测试上滑卡片（超级喜欢）"""
        response = client.post(
            "/api/v1/match/swipe",
            json={
                "cardId": "card_003",
                "direction": "up"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "isMatch" in data["data"]
