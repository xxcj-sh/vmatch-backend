"""
测试工具
提供便捷的测试模式控制和测试数据生成功能
"""
from app.config import settings
from app.utils.test_data_generator import test_data_generator
from typing import Dict, Any, Optional, List, Union

class TestUtils:
    """测试工具类"""
    
    @staticmethod
    def enable_test_mode():
        """启用测试模式"""
        settings.test_mode = True
        print("Test mode enabled")
    
    @staticmethod
    def disable_test_mode():
        """禁用测试模式"""
        settings.test_mode = False
        print("Test mode disabled")
    
    @staticmethod
    def is_test_mode() -> bool:
        """检查是否处于测试模式"""
        return settings.test_mode
    
    # 固定测试用户相关方法
    @staticmethod
    def get_fixed_test_user() -> Dict[str, Any]:
        """获取固定的测试用户数据"""
        return {
            "id": "test_user_001",
            "nickName": "测试用户",
            "avatarUrl": "https://picsum.photos/200/200?random=test-avatar",
            "gender": 1,
            "age": 30,
            "occupation": "软件工程师",
            "location": "上海",
            "bio": "这是一个测试账号，用于开发和测试微信小程序",
            "education": "本科",
            "interests": ["编程", "测试", "开发"],
            "joinDate": 1628553600,
            "phone": "13800138000",
            "email": "test@example.com",
            "matchType": "dating",
            "userRole": "user",
            "preferences": {
                "ageRange": [25, 35],
                "distance": 20
            }
        }
    
    @staticmethod
    def get_fixed_test_token() -> str:
        """获取固定的测试Token"""
        return "test_token_001"
    
    @staticmethod
    def get_fixed_test_headers() -> Dict[str, str]:
        """获取固定的测试请求头"""
        return {"Authorization": f"Bearer {TestUtils.get_fixed_test_token()}"}
    
    @staticmethod
    def generate_test_data(api_path: str, method: str = "GET", params: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成指定API的测试数据"""
        return test_data_generator.mock_api_response(api_path, method, params)
    
    @staticmethod
    def generate_user_data(user_id: str = "") -> Dict[str, Any]:
        """生成用户测试数据"""
        return test_data_generator.generate_user(user_id)
    
    @staticmethod
    def generate_card_data(card_id: str = "") -> Dict[str, Any]:
        """生成卡片测试数据"""
        return test_data_generator.generate_card(card_id)
    
    @staticmethod
    def generate_match_data(match_id: str = "", user_id: str = "", card_id: str = "") -> Dict[str, Any]:
        """生成匹配测试数据"""
        return test_data_generator.generate_match(match_id, user_id, card_id)
    
    @staticmethod
    def generate_message_data(message_id: str = "", match_id: str = "", sender_id: str = "") -> Dict[str, Any]:
        """生成消息测试数据"""
        return test_data_generator.generate_message(message_id, match_id, sender_id)
    
    @staticmethod
    def generate_membership_data(user_id: str = "") -> Dict[str, Any]:
        """生成会员测试数据"""
        return test_data_generator.generate_membership_info(user_id)
    
    @staticmethod
    def generate_payment_data(order_id: str = "", user_id: str = "") -> Dict[str, Any]:
        """生成支付测试数据"""
        return test_data_generator.generate_payment_info(order_id, user_id)
    
    @staticmethod
    def generate_test_token(user_id: str = "user_001") -> str:
        """生成测试用户Token"""
        return f"test_token_{user_id}"
    
    @staticmethod
    def get_test_headers(user_id: str = "user_001") -> Dict[str, str]:
        """获取测试请求头（包含认证信息）"""
        token = TestUtils.generate_test_token(user_id)
        return {"Authorization": f"Bearer {token}"}

# 创建单例实例
test_utils = TestUtils()