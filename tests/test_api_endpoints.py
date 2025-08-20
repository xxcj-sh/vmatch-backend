import pytest
from fastapi.testclient import TestClient
from app.main import app
import io
from PIL import Image

client = TestClient(app)

# 测试用户Token
TEST_TOKEN = "user_001"
AUTH_HEADER = {"Authorization": f"Bearer {TEST_TOKEN}"}

class TestAuthEndpoints:
    """测试认证相关接口"""
    
    def test_login(self):
        """测试微信登录接口"""
        response = client.post(
            "/api/v1/auth/login",
            json={"code": "test_code", "userInfo": {"nickName": "测试用户", "avatarUrl": "https://example.com/avatar.jpg", "gender": 1}}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "token" in data["data"]
        assert "userInfo" in data["data"]
    
    def test_login_by_phone(self):
        """测试手机号登录接口"""
        # 先发送验证码
        response = client.post(
            "/api/v1/auth/sms-code",
            json={"phone": "13800138000"}
        )
        assert response.status_code == 200
        
        # 然后登录
        response = client.post(
            "/api/v1/auth/login/phone",
            json={"phone": "13800138000", "code": "123456"}  # 测试模式下任意验证码
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "token" in data["data"]
    
    def test_validate_token(self):
        """测试验证Token接口"""
        response = client.get(
            "/api/v1/auth/validate",
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["valid"] is True

class TestUserEndpoints:
    """测试用户相关接口"""
    
    def test_get_user_info(self):
        """测试获取用户信息接口"""
        response = client.get(
            "/api/v1/user/info",
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "id" in data["data"]
        assert "nickName" in data["data"]
    
    def test_get_user_profile(self):
        """测试获取他人用户资料接口"""
        # 先创建一个测试用户
        response = client.get(
            "/api/v1/user/profile/card_001",
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "nickname" in data["data"] or "name" in data["data"]
        assert "avatar" in data["data"]
    
    def test_get_user_stats(self):
        """测试获取用户统计数据接口"""
        response = client.get(
            "/api/v1/user/stats",
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "matchCount" in data["data"]
        assert "messageCount" in data["data"]
        assert "favoriteCount" in data["data"]

class TestProfileEndpoints:
    """测试个人资料相关接口"""
    
    def test_get_profile(self):
        """测试获取个人资料接口"""
        response = client.get(
            "/api/v1/profile/get",
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "id" in data["data"]
        assert "nickName" in data["data"]
    
    def test_update_profile(self):
        """测试更新个人资料接口"""
        response = client.post(
            "/api/v1/profile/update",
            headers=AUTH_HEADER,
            json={
                "nickName": "新昵称",
                "bio": "新的个人简介"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["success"] == True

class TestMatchEndpoints:
    """测试匹配相关接口"""
    
    def test_get_match_cards(self):
        """测试获取匹配卡片接口"""
        response = client.get(
            "/api/v1/match/cards?type=dating&userRole=seeker&page=1&pageSize=10",
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "total" in data["data"]
        assert "list" in data["data"]
    
    def test_submit_match_action(self):
        """测试提交匹配操作接口"""
        response = client.post(
            "/api/v1/match/action",
            headers=AUTH_HEADER,
            json={
                "cardId": "card_002",
                "action": "like",
                "matchType": "dating"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "isMatch" in data["data"]
    
    def test_get_match_list(self):
        """测试获取匹配列表接口"""
        response = client.get(
            "/api/v1/match/list?status=all&page=1&pageSize=10",
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "total" in data["data"]
        assert "list" in data["data"]

class TestChatEndpoints:
    """测试聊天相关接口"""
    
    def test_get_chat_history(self):
        """测试获取聊天记录接口"""
        response = client.get(
            "/api/v1/chat/history/match_001?page=1&limit=20",
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "total" in data["data"]
        assert "list" in data["data"]
    
    def test_send_message(self):
        """测试发送消息接口"""
        response = client.post(
            "/api/v1/chat/send",
            headers=AUTH_HEADER,
            json={
                "matchId": "match_001",
                "content": "你好，这是一条测试消息",
                "type": "text"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "id" in data["data"]
        assert "timestamp" in data["data"]
    
    def test_mark_messages_read(self):
        """测试标记消息已读接口"""
        response = client.post(
            "/api/v1/chat/read",
            headers=AUTH_HEADER,
            json={
                "matchId": "match_001"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["success"] == True

class TestFileEndpoints:
    """测试文件上传相关接口"""
    
    def test_upload_image(self):
        """测试上传图片接口"""
        # 创建一个测试图片文件
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'jpeg')
        file.name = 'test.jpg'
        file.seek(0)
        
        response = client.post(
            "/api/v1/upload/image",
            headers=AUTH_HEADER,
            files={"file": ("test.jpg", file, "image/jpeg")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "url" in data["data"]

class TestMembershipEndpoints:
    """测试会员相关接口"""
    
    def test_get_membership_info(self):
        """测试获取会员信息接口"""
        response = client.get(
            "/api/v1/membership/info",
            headers=AUTH_HEADER
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "level" in data["data"]
        assert "features" in data["data"]
    
    def test_create_membership_payment(self):
        """测试创建会员支付接口"""
        response = client.post(
            "/api/v1/membership/payment",
            headers=AUTH_HEADER,
            json={
                "planId": "premium_monthly"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "orderId" in data["data"]
        assert "paymentUrl" in data["data"]