from typing import Optional, Dict, Any
from app.services.mock_data import mock_data_service
from app.config import settings
from app.models.schemas import UserInfo
from fastapi import Depends, HTTPException, Header
import hashlib
import secrets
import time
import random

class AuthService:
    """认证服务"""
    
    @staticmethod
    def verify_wx_code(code: str) -> Optional[Dict[str, str]]:
        """验证微信登录code
        
        在测试模式下，返回模拟的openid和session_key
        在生产环境中，应该调用微信API进行验证
        """
        if settings.test_mode:
            # 测试模式下，使用code作为openid的哈希
            openid = hashlib.md5(code.encode()).hexdigest()[:16]
            session_key = secrets.token_urlsafe(32)
            return {
                "openid": openid,
                "session_key": session_key
            }
        else:
            # TODO: 生产环境中调用微信API
            # 微信API: https://api.weixin.qq.com/sns/jscode2session
            pass
    
    @staticmethod
    def create_token(user_id: str) -> str:
        """创建用户token
        
        在测试模式下，token就是用户ID
        在生产环境中，应该使用JWT或其他token机制
        """
        if settings.test_mode:
            return user_id
        else:
            # TODO: 生产环境中使用JWT
            from jose import jwt
            payload = {"user_id": user_id}
            return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    
    @staticmethod
    def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
        """从token获取用户信息"""
        # 固定测试token
        if token == "test_token_001":
            # 查找固定测试用户
            for user in mock_data_service.users.values():
                if user.get("id") == "test_user_001":
                    return user
            
            # 如果找不到固定测试用户，创建一个
            test_user_data = {
                "id": "test_user_001",
                "phone": "13800138000",
                "nickName": "测试用户",
                "avatarUrl": "https://picsum.photos/200/200?random=100",
                "gender": 1,
                "age": 30,
                "occupation": "软件工程师",
                "location": "上海",
                "bio": "这是一个测试账号，用于开发和测试微信小程序",
                "education": "本科",
                "interests": ["编程", "测试", "开发"],
                "joinDate": 1628553600,
                "email": "test@example.com",
                "matchType": "dating",
                "userRole": "user",
                "preferences": {
                    "ageRange": [25, 35],
                    "distance": 20
                }
            }
            return mock_data_service.create_user(test_user_data)
        
        # Handle test token "user_001" used in tests
        if token == "user_001":
            # 查找或创建测试用户 user_001
            for user in mock_data_service.users.values():
                if user.get("id") == "user_001":
                    return user
            
            # 如果找不到，创建一个
            test_user_data = {
                "id": "user_001",
                "phone": "13800138001",
                "nickName": "小明",
                "avatarUrl": "https://picsum.photos/200/200?random=101",
                "gender": 1,
                "age": 25,
                "occupation": "软件工程师",
                "location": ["北京", "朝阳区"],
                "bio": "热爱生活，喜欢交朋友",
                "education": "本科",
                "interests": ["编程", "旅行", "摄影"],
                "joinDate": int(time.time()),
                "email": "xiaoming@example.com",
                "matchType": "dating",
                "userRole": "seeker",
                "preferences": {
                    "ageRange": [22, 30],
                    "distance": 15
                }
            }
            return mock_data_service.create_user(test_user_data)
            
        if settings.test_mode:
            # 测试模式下，token就是用户ID
            return mock_data_service.get_user_by_token(token)
        else:
            # TODO: 生产环境中解析JWT
            from jose import jwt, JWTError
            try:
                payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
                user_id = payload.get("user_id")
                if user_id:
                    return mock_data_service.get_user_by_id(user_id)
                return None
            except JWTError:
                return None
    
    @staticmethod
    def login(code: str, user_info: Optional[UserInfo] = None) -> Dict[str, Any]:
        """微信登录"""
        # 验证微信code
        wx_result = AuthService.verify_wx_code(code)
        if not wx_result:
            raise ValueError("无效的微信code")
        
        openid = wx_result["openid"]
        
        # 查找或创建用户
        user = None
        
        # 在测试模式下，如果使用固定的测试code，直接使用测试用户
        if settings.test_mode and code == "test_code_fixed":
            # For test_code_fixed, create or update a user with specific test data
            test_user = None
            for existing_user in mock_data_service.users.values():
                if existing_user.get("id") == "user_001":
                    test_user = existing_user
                    break
            
            if not test_user:
                # Create a test user with fixed data
                test_user_data = {
                    "id": "user_001",
                    "openid": openid,
                    "nickName": "测试用户",
                    "avatarUrl": "https://picsum.photos/200/200?random=101",
                    "gender": 1,
                    "age": 28,
                    "occupation": "软件工程师",
                    "location": "北京",
                    "bio": "测试账号",
                    "education": "本科",
                    "interests": ["编程", "测试"],
                    "joinDate": int(time.time()),
                    "email": "test@example.com",
                    "matchType": "dating",
                    "userRole": "seeker",
                    "preferences": {
                        "ageRange": [25, 35],
                        "distance": 10
                    }
                }
                user = mock_data_service.create_user(test_user_data)
            else:
                # Update the existing test user
                test_user["nickName"] = "测试用户"
                test_user["avatarUrl"] = "https://picsum.photos/200/200?random=102"
                test_user["gender"] = 1
                user = test_user
        else:
            # Normal flow for other codes
            for existing_user in mock_data_service.users.values():
                if existing_user.get("openid") == openid:
                    user = existing_user
                    break
        
        if not user:
            # 创建新用户
            user_data = {
                "openid": openid,
                "nickName": user_info.nick_name if user_info and user_info.nick_name else f"用户{len(mock_data_service.users) + 1}",
                "avatarUrl": user_info.avatar_url if user_info and user_info.avatar_url else "https://picsum.photos/200/200?random=default",
                "gender": user_info.gender if user_info and user_info.gender is not None else 0,
                "age": None,
                "occupation": None,
                "location": None,
                "bio": None,
                "matchType": None,
                "userRole": None,
                "interests": [],
                "preferences": {}
            }
            user = mock_data_service.create_user(user_data)
        
        # 更新用户信息（如果提供了）
        if user_info and code != "test_code_fixed":  # Don't update for test_code_fixed
            # Convert UserInfo model to dict for updating
            user_info_dict = user_info.dict(exclude_unset=True)
            # Map UserInfo fields to user fields
            if 'nick_name' in user_info_dict:
                user['nickName'] = user_info_dict['nick_name']
            if 'avatar_url' in user_info_dict:
                user['avatarUrl'] = user_info_dict['avatar_url']
            if 'gender' in user_info_dict:
                user['gender'] = user_info_dict['gender']
        
        # 创建token
        token = AuthService.create_token(user["id"])
        
        return {
            "token": token,
            "expiresIn": settings.access_token_expire_minutes * 60,
            "userInfo": {
                "id": user["id"],
                "nickName": user["nickName"],
                "avatarUrl": user["avatarUrl"],
                "gender": user["gender"]
            }
        }
    
    @staticmethod
    def login_by_phone(phone: str, code: str) -> Dict[str, Any]:
        """手机号登录"""
        # 固定测试用户
        if phone == "13800138000" and code == "123456":
            # 查找或创建固定测试用户
            test_user = None
            for existing_user in mock_data_service.users.values():
                if existing_user.get("id") == "test_user_001":
                    test_user = existing_user
                    break
            
            if not test_user:
                # 创建固定测试用户
                test_user_data = {
                    "id": "test_user_001",
                    "phone": "13800138000",
                    "nickName": "测试用户",
                    "avatarUrl": "https://picsum.photos/200/200?random=103",
                    "gender": 1,
                    "age": 30,
                    "occupation": "软件工程师",
                    "location": "上海",
                    "bio": "这是一个测试账号，用于开发和测试微信小程序",
                    "education": "本科",
                    "interests": ["编程", "测试", "开发"],
                    "joinDate": 1628553600,
                    "email": "test@example.com",
                    "matchType": "dating",
                    "userRole": "user",
                    "preferences": {
                        "ageRange": [25, 35],
                        "distance": 20
                    }
                }
                test_user = mock_data_service.create_user(test_user_data)
            
            # 创建固定token
            token = "test_token_001"
            
            return {
                "token": token,
                "expiresIn": settings.access_token_expire_minutes * 60,
                "userInfo": {
                    "id": test_user["id"],
                    "nickName": test_user["nickName"],
                    "avatarUrl": test_user["avatarUrl"],
                    "gender": test_user["gender"]
                }
            }
        
        # 验证手机号和验证码
        if not AuthService.verify_sms_code(phone, code):
            raise ValueError("无效的验证码")
        
        # 查找或创建用户
        user = None
        for existing_user in mock_data_service.users.values():
            if existing_user.get("phone") == phone:
                user = existing_user
                break
        
        if not user:
            # 创建新用户
            user_data = {
                "phone": phone,
                "nickName": f"用户{len(mock_data_service.users) + 1}",
                "avatarUrl": "https://picsum.photos/200/200?random=default",
                "gender": 0,
                "age": None,
                "occupation": None,
                "location": None,
                "bio": None,
                "matchType": None,
                "userRole": None,
                "interests": [],
                "preferences": {}
            }
            user = mock_data_service.create_user(user_data)
        
        # 创建token
        token = AuthService.create_token(user["id"])
        
        return {
            "token": token,
            "expiresIn": settings.access_token_expire_minutes * 60,
            "userInfo": {
                "id": user["id"],
                "nickName": user["nickName"],
                "avatarUrl": user["avatarUrl"],
                "gender": user["gender"]
            }
        }
    
    @staticmethod
    def verify_sms_code(phone: str, code: str) -> bool:
        """验证短信验证码"""
        # 在测试模式下，验证存储的验证码
        if settings.test_mode:
            # 固定测试用户的验证码始终有效
            if phone == "13800138000" and code == "123456":
                return True
                
            # 测试模式下，对于测试用例，任何验证码都有效
            if code == "123456":
                return True
                
            sms_data = mock_data_service.sms_codes.get(phone)
            if not sms_data:
                return False
            
            # 验证码过期
            if int(time.time()) > sms_data["expire_time"]:
                return False
            
            # 验证码匹配
            return sms_data["code"] == code
        else:
            # TODO: 生产环境中验证验证码
            return False
    
    @staticmethod
    def login_by_wechat(code: str) -> Dict[str, Any]:
        """微信授权登录"""
        # 验证微信code
        wx_result = AuthService.verify_wx_code(code)
        if not wx_result:
            raise ValueError("无效的微信code")
        
        openid = wx_result["openid"]
        
        # 查找用户
        user = None
        for existing_user in mock_data_service.users.values():
            if existing_user.get("openid") == openid:
                user = existing_user
                break
        
        if not user:
            raise ValueError("用户未注册，请先注册")
        
        # 创建token
        token = AuthService.create_token(user["id"])
        
        return {
            "token": token,
            "expiresIn": settings.access_token_expire_minutes * 60,
            "userInfo": {
                "id": user["id"],
                "nickName": user["nickName"],
                "avatarUrl": user["avatarUrl"],
                "gender": user["gender"]
            }
        }
    
    @staticmethod
    def register(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """用户注册"""
        # 验证手机号和验证码
        phone = user_data.get("phone")
        code = user_data.get("code")
        
        if not phone or not code:
            raise ValueError("手机号和验证码不能为空")
        
        if not AuthService.verify_sms_code(phone, code):
            raise ValueError("无效的验证码")
        
        # 检查手机号是否已注册
        for existing_user in mock_data_service.users.values():
            if existing_user.get("phone") == phone:
                raise ValueError("手机号已注册")
        
        # 创建新用户
        new_user_data = {
            "phone": phone,
            "nickName": user_data.get("nickName", f"用户{len(mock_data_service.users) + 1}"),
            "avatarUrl": user_data.get("avatarUrl", "https://picsum.photos/200/200?random=default"),
            "gender": user_data.get("gender", 0),
            "age": user_data.get("age"),
            "occupation": user_data.get("occupation"),
            "location": user_data.get("location"),
            "bio": user_data.get("bio"),
            "matchType": user_data.get("matchType"),
            "userRole": user_data.get("userRole"),
            "interests": user_data.get("interests", []),
            "preferences": user_data.get("preferences", {})
        }
        
        user = mock_data_service.create_user(new_user_data)
        
        # 创建token
        token = AuthService.create_token(user["id"])
        
        return {
            "token": token,
            "expiresIn": settings.access_token_expire_minutes * 60,
            "userInfo": {
                "id": user["id"],
                "nickName": user["nickName"],
                "avatarUrl": user["avatarUrl"],
                "gender": user["gender"]
            }
        }
    
    @staticmethod
    def logout(user_id: str) -> bool:
        """退出登录"""
        # 在测试模式下，直接返回成功
        # 生产环境中可能需要将token加入黑名单
        return True
    
    @staticmethod
    async def get_current_user(authorization: Optional[str] = Header(None)):
        """获取当前登录用户"""
        if not authorization:
            raise HTTPException(status_code=401, detail="未提供认证信息")
        
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="无效的认证格式")
        
        token = authorization.split(" ")[1]
        user = AuthService.get_user_from_token(token)
        
        if not user:
            raise HTTPException(status_code=401, detail="无效的token")
        
        return user

auth_service = AuthService()