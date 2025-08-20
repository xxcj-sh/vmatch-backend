import pytest
from fastapi.testclient import TestClient

class TestIntegration:
    """集成测试"""
    
    def test_complete_user_flow(self, client: TestClient):
        """测试完整用户流程"""
        
        # 1. 用户登录
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "code": "integration_test_code",
                "userInfo": {
                    "nickName": "集成测试用户",
                    "avatarUrl": "https://picsum.photos/200/200?random=integration",
                    "gender": 1
                }
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["data"]["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. 获取用户信息
        user_response = client.get("/api/v1/user/info", headers=headers)
        assert user_response.status_code == 200
        
        # 3. 获取匹配卡片
        cards_response = client.get(
            "/api/v1/match/cards?matchType=dating&userRole=seeker&page=1&pageSize=5",
            headers=headers
        )
        assert cards_response.status_code == 200
        cards = cards_response.json()["data"]["list"]
        assert len(cards) > 0
        
        # 4. 进行匹配操作
        action_response = client.post(
            "/api/v1/match/action",
            json={
                "cardId": cards[0]["id"],
                "action": "like",
                "matchType": "dating"
            },
            headers=headers
        )
        assert action_response.status_code == 200
        
        # 5. 获取匹配列表
        matches_response = client.get("/api/v1/match/list?status=all&page=1&pageSize=10", headers=headers)
        assert matches_response.status_code == 200
        matches = matches_response.json()["data"]["list"]
        
        if matches:
            match_id = matches[0]["id"]
            
            # 6. 发送消息
            message_response = client.post(
                "/api/v1/chat/send",
                json={
                    "matchId": match_id,
                    "content": "这是一条集成测试消息",
                    "type": "text"
                },
                headers=headers
            )
            assert message_response.status_code == 200
            
            # 7. 获取聊天记录
            history_response = client.get(
                f"/api/v1/chat/history?matchId={match_id}&page=1&pageSize=20",
                headers=headers
            )
            assert history_response.status_code == 200
            messages = history_response.json()["data"]["list"]
            assert len(messages) > 0
        
        # 8. 更新个人资料
        profile_response = client.put(
            "/api/v1/profile",
            json={
                "bio": "这是集成测试的更新",
                "age": 30,
                "occupation": "测试工程师"
            },
            headers=headers
        )
        assert profile_response.status_code == 200
        
        # 9. 获取更新后的个人资料
        updated_profile = client.get("/api/v1/profile", headers=headers)
        assert updated_profile.status_code == 200
        assert updated_profile.json()["data"]["bio"] == "这是集成测试的更新"