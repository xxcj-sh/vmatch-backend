"""
RESTful API 测试
测试新的 RESTful API 设计
"""
import pytest
import requests
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestRESTfulAPI:
    """RESTful API 测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.test_headers = {"X-Test-Mode": "true"}
        self.auth_headers = {
            "X-Test-Mode": "true",
            "Authorization": "Bearer user_001"
        }
    
    def test_api_info(self):
        """测试 API 信息端点"""
        response = client.get("/api/v1", headers=self.test_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["version"] == "2.0.0"
        assert data["design"] == "RESTful"
        assert "endpoints" in data
    
    # Authentication Tests
    def test_create_session_success(self):
        """测试创建会话成功"""
        payload = {
            "code": "test_wx_code",
            "userInfo": {
                "nickName": "测试用户",
                "avatarUrl": "https://example.com/avatar.jpg",
                "gender": 1
            }
        }
        response = client.post("/api/v1/auth/sessions", 
                             json=payload, 
                             headers=self.test_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "success"
        assert "token" in data["data"]
        assert "user" in data["data"]
        assert "timestamp" in data
    
    def test_create_session_missing_code(self):
        """测试创建会话缺少code"""
        payload = {}
        response = client.post("/api/v1/auth/sessions", 
                             json=payload, 
                             headers=self.test_headers)
        assert response.status_code == 422
        data = response.json()
        assert data["code"] == 422
        assert "code" in data["message"]
    
    def test_create_phone_session(self):
        """测试手机号创建会话"""
        payload = {
            "phone": "13800138000",
            "code": "123456"
        }
        response = client.post("/api/v1/auth/sessions/phone", 
                             json=payload, 
                             headers=self.test_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert "token" in data["data"]
    
    def test_send_sms_code(self):
        """测试发送短信验证码"""
        payload = {"phone": "13800138000"}
        response = client.post("/api/v1/auth/sms-codes", 
                             json=payload, 
                             headers=self.test_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["sent"] == True
    
    def test_validate_current_session(self):
        """测试验证当前会话"""
        response = client.get("/api/v1/auth/sessions/current", 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["valid"] == True
        assert "user" in data["data"]
    
    def test_delete_current_session(self):
        """测试删除当前会话（登出）"""
        response = client.delete("/api/v1/auth/sessions/current", 
                               headers=self.auth_headers)
        assert response.status_code == 204
    
    # User Tests
    def test_get_current_user(self):
        """测试获取当前用户信息"""
        response = client.get("/api/v1/users/me", 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "id" in data["data"]
        assert "nickName" in data["data"]
        assert "createdAt" in data["data"]
    
    def test_update_current_user(self):
        """测试更新当前用户信息"""
        payload = {
            "nickName": "更新的用户名",
            "avatarUrl": "https://example.com/new_avatar.jpg"
        }
        response = client.put("/api/v1/users/me", 
                            json=payload, 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["nickName"] == "更新的用户名"
    
    def test_get_user_by_id(self):
        """测试根据ID获取用户信息"""
        response = client.get("/api/v1/users/user_002", 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["id"] == "user_002"
        assert "nickname" in data["data"]
    
    def test_get_user_stats(self):
        """测试获取用户统计信息"""
        response = client.get("/api/v1/users/me/stats", 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "matchCount" in data["data"]
        assert "messageCount" in data["data"]
    
    # Profile Tests
    def test_get_current_profile(self):
        """测试获取当前用户资料"""
        response = client.get("/api/v1/profiles/me", 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "id" in data["data"]
        assert "interests" in data["data"]
    
    def test_update_current_profile(self):
        """测试更新当前用户资料"""
        payload = {
            "age": 26,
            "occupation": "高级软件工程师",
            "bio": "更新的个人简介",
            "interests": ["音乐", "旅行", "摄影", "编程"]
        }
        response = client.put("/api/v1/profiles/me", 
                            json=payload, 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["age"] == 26
        assert data["data"]["bio"] == "更新的个人简介"
    
    # Match Tests
    def test_get_match_cards(self):
        """测试获取匹配卡片"""
        params = {
            "matchType": "housing",
            "userRole": "seeker",
            "page": 1,
            "pageSize": 10
        }
        response = client.get("/api/v1/matches/cards", 
                            params=params, 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "cards" in data["data"]
        assert "pagination" in data["data"]
    
    def test_create_match_action(self):
        """测试创建匹配操作"""
        payload = {
            "cardId": "card_001",
            "action": "like",
            "matchType": "housing"
        }
        response = client.post("/api/v1/matches/actions", 
                             json=payload, 
                             headers=self.auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert "isMatch" in data["data"]
    
    def test_swipe_card(self):
        """测试滑动卡片"""
        payload = {
            "cardId": "card_001",
            "direction": "right"
        }
        response = client.post("/api/v1/matches/swipes", 
                             json=payload, 
                             headers=self.auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert "isMatch" in data["data"]
    
    def test_get_matches(self):
        """测试获取匹配列表"""
        params = {
            "status": "all",
            "page": 1,
            "pageSize": 10
        }
        response = client.get("/api/v1/matches", 
                            params=params, 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "matches" in data["data"]
        assert "pagination" in data["data"]
    
    def test_get_match_detail(self):
        """测试获取匹配详情"""
        response = client.get("/api/v1/matches/match_001", 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["id"] == "match_001"
        assert "user" in data["data"]
    
    # Message Tests
    def test_get_messages(self):
        """测试获取消息列表"""
        params = {
            "matchId": "match_001",
            "page": 1,
            "limit": 20
        }
        response = client.get("/api/v1/messages", 
                            params=params, 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "messages" in data["data"]
        assert "pagination" in data["data"]
    
    def test_send_message(self):
        """测试发送消息"""
        payload = {
            "matchId": "match_001",
            "content": "你好，很高兴认识你！",
            "type": "text"
        }
        response = client.post("/api/v1/messages", 
                             json=payload, 
                             headers=self.auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert "id" in data["data"]
        assert "timestamp" in data["data"]
    
    def test_mark_messages_read(self):
        """测试标记消息已读"""
        payload = {"matchId": "match_001"}
        response = client.put("/api/v1/messages/read", 
                            json=payload, 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["success"] == True
    
    # File Tests
    def test_upload_file(self):
        """测试文件上传"""
        # 创建测试文件
        test_file_content = b"fake image content"
        files = {
            "file": ("test.jpg", test_file_content, "image/jpeg")
        }
        data = {"type": "avatar"}
        
        response = client.post("/api/v1/files", 
                             files=files, 
                             data=data, 
                             headers=self.auth_headers)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["code"] == 0
        assert "url" in response_data["data"]
    
    # Membership Tests
    def test_get_membership(self):
        """测试获取会员信息"""
        response = client.get("/api/v1/memberships/me", 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "level" in data["data"]
        assert "features" in data["data"]
    
    def test_create_membership_order(self):
        """测试创建会员订单"""
        payload = {"planId": "premium_monthly"}
        response = client.post("/api/v1/memberships/orders", 
                             json=payload, 
                             headers=self.auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert "orderId" in data["data"]
        assert "paymentUrl" in data["data"]
    
    # Property Tests
    def test_get_property_detail(self):
        """测试获取房源详情"""
        response = client.get("/api/v1/properties/property_001", 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["id"] == "property_001"
        assert "title" in data["data"]
        assert "price" in data["data"]
    
    # Scene Tests
    def test_get_scenes(self):
        """测试获取场景配置"""
        response = client.get("/api/v1/scenes", 
                            headers=self.test_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "scenes" in data["data"]
    
    def test_get_scene_by_key(self):
        """测试根据key获取场景配置"""
        response = client.get("/api/v1/scenes/housing", 
                            headers=self.test_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["key"] == "housing"
    
    # Error Handling Tests
    def test_unauthorized_access(self):
        """测试未授权访问"""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401
    
    def test_invalid_endpoint(self):
        """测试无效端点"""
        response = client.get("/api/v1/invalid", 
                            headers=self.test_headers)
        assert response.status_code == 404
    
    def test_missing_required_params(self):
        """测试缺少必要参数"""
        response = client.get("/api/v1/matches/cards", 
                            headers=self.auth_headers)
        assert response.status_code == 422
        data = response.json()
        assert data["code"] == 422
        assert "必要参数" in data["message"]
    
    # Response Format Tests
    def test_response_format_consistency(self):
        """测试响应格式一致性"""
        response = client.get("/api/v1/users/me", 
                            headers=self.auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # 检查标准响应格式
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data
        
        # 检查时间戳格式
        import datetime
        try:
            datetime.datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            pytest.fail("Invalid timestamp format")
    
    def test_http_status_codes(self):
        """测试HTTP状态码正确性"""
        # 200 OK for GET
        response = client.get("/api/v1/users/me", headers=self.auth_headers)
        assert response.status_code == 200
        
        # 201 Created for POST
        payload = {"code": "test_code"}
        response = client.post("/api/v1/auth/sessions", 
                             json=payload, headers=self.test_headers)
        assert response.status_code == 201
        
        # 401 Unauthorized
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401
        
        # 422 Validation Error
        response = client.post("/api/v1/auth/sessions", 
                             json={}, headers=self.test_headers)
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])