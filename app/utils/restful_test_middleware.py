"""
RESTful API 测试中间件
支持新的 RESTful API 设计和 X-Test-Mode 头部
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.config import settings
from app.utils.test_data_generator import test_data_generator
import json
import time
import os
from datetime import datetime, timezone

class RESTfulTestModeMiddleware(BaseHTTPMiddleware):
    """RESTful 测试模式中间件，支持 X-Test-Mode 头部"""
    
    def __init__(self, app):
        super().__init__(app)
        self.test_users = {
            "user_001": {
                "id": "user_001",
                "nickName": "测试用户1",
                "avatarUrl": "https://picsum.photos/200/200?random=1",
                "phone": "13800138001",
                "gender": 1,
                "age": 25,
                "occupation": "软件工程师",
                "location": ["北京", "朝阳区"],
                "bio": "这是测试用户1的简介",
                "interests": ["音乐", "旅行", "摄影"],
                "preferences": {"ageRange": [20, 30]},
                "createdAt": "2024-01-01T00:00:00Z"
            },
            "user_002": {
                "id": "user_002",
                "nickName": "测试用户2",
                "avatarUrl": "https://picsum.photos/200/200?random=2",
                "phone": "13800138002",
                "gender": 2,
                "age": 28,
                "occupation": "设计师",
                "location": ["上海", "浦东新区"],
                "bio": "这是测试用户2的简介",
                "interests": ["设计", "艺术", "电影"],
                "preferences": {"ageRange": [25, 35]},
                "createdAt": "2024-01-01T00:00:00Z"
            }
        }
    
    def is_test_mode(self, request: Request) -> bool:
        """检查是否为测试模式"""
        return (
            settings.test_mode or 
            request.headers.get("X-Test-Mode", "").lower() == "true"
        )
    
    def get_current_timestamp(self) -> str:
        """获取当前时间戳"""
        return datetime.now(timezone.utc).isoformat()
    
    def create_response(self, code: int = 0, message: str = "success", data=None, status_code: int = 200):
        """创建标准响应格式"""
        return JSONResponse(
            status_code=status_code,
            content={
                "code": code,
                "message": message,
                "data": data,
                "timestamp": self.get_current_timestamp()
            }
        )
    
    def get_test_user_from_token(self, token: str):
        """从测试 token 获取用户信息"""
        # 在测试模式下，token 就是用户ID
        return self.test_users.get(token, self.test_users.get("user_001"))
    
    async def dispatch(self, request: Request, call_next):
        """处理请求"""
        # 如果不是测试模式，直接传递给下一个中间件
        if not self.is_test_mode(request):
            return await call_next(request)

        # 获取请求路径和方法
        path = request.url.path
        method = request.method
        
        # 只处理API请求
        if not path.startswith("/api/v1/"):
            return await call_next(request)
        
        # 在测试模式下，只有提供了正确的认证头才获取用户信息
        auth_header = request.headers.get("authorization", "")
        current_user = None
        
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            current_user = self.get_test_user_from_token(token)
        
        # 处理新的 RESTful API 端点
        try:
            response = await self.handle_restful_endpoints(request, path, method, current_user)
            if response:
                return response
        except Exception as e:
            return self.create_response(
                code=500,
                message=f"Internal server error: {str(e)}",
                status_code=500
            )
        
        # 如果没有匹配的端点，传递给实际路由
        return await call_next(request)
    
    def requires_auth(self, path: str) -> bool:
        """检查路径是否需要认证"""
        public_paths = [
            "/api/v1/auth/sessions",
            "/api/v1/auth/sessions/phone",
            "/api/v1/auth/sms-codes",
            "/api/v1/scenes"
        ]
        return not any(path.startswith(p) for p in public_paths)
    
    async def handle_restful_endpoints(self, request: Request, path: str, method: str, current_user):
        """处理 RESTful API 端点"""
        
        # Authentication endpoints
        if path == "/api/v1/auth/sessions" and method == "POST":
            return await self.handle_login(request)
        
        if path == "/api/v1/auth/sessions/phone" and method == "POST":
            return await self.handle_phone_login(request)
        
        if path == "/api/v1/auth/sms-codes" and method == "POST":
            return await self.handle_sms_code(request)
        
        if path == "/api/v1/auth/sessions/current" and method == "GET":
            return self.handle_validate_session(current_user)
        
        if path == "/api/v1/auth/sessions/current" and method == "DELETE":
            return self.create_response(message="Logged out successfully", status_code=204)
        
        # User endpoints - more specific routes first
        if path == "/api/v1/users/me/stats" and method == "GET":
            return self.handle_get_user_stats(current_user)
        
        if path == "/api/v1/users/me" and method == "GET":
            return self.handle_get_current_user(current_user)
        
        if path == "/api/v1/users/me" and method == "PUT":
            return await self.handle_update_current_user(request, current_user)
        
        if path.startswith("/api/v1/users/") and method == "GET":
            user_id = path.split("/")[-1]
            return self.handle_get_user_by_id(user_id)
        
        # Profile endpoints
        if path == "/api/v1/profiles/me" and method == "GET":
            return self.handle_get_profile(current_user)
        
        if path == "/api/v1/profiles/me" and method == "PUT":
            return await self.handle_update_profile(request, current_user)
        
        # Match endpoints
        if path == "/api/v1/matches/cards" and method == "GET":
            return await self.handle_get_match_cards(request, current_user)
        
        if path == "/api/v1/matches/actions" and method == "POST":
            return await self.handle_match_action(request, current_user)
        
        if path == "/api/v1/matches/swipes" and method == "POST":
            return await self.handle_swipe_card(request, current_user)
        
        if path == "/api/v1/matches" and method == "GET":
            return await self.handle_get_matches(request, current_user)
        
        if path.startswith("/api/v1/matches/") and method == "GET":
            match_id = path.split("/")[-1]
            return self.handle_get_match_detail(match_id, current_user)
        
        # Message endpoints
        if path == "/api/v1/messages" and method == "GET":
            return await self.handle_get_messages(request, current_user)
        
        if path == "/api/v1/messages" and method == "POST":
            return await self.handle_send_message(request, current_user)
        
        if path == "/api/v1/messages/read" and method == "PUT":
            return await self.handle_mark_messages_read(request, current_user)
        
        # File endpoints
        if path == "/api/v1/files" and method == "POST":
            return await self.handle_file_upload(request, current_user)
        
        # Membership endpoints
        if path == "/api/v1/memberships/me" and method == "GET":
            return self.handle_get_membership(current_user)
        
        if path == "/api/v1/memberships/orders" and method == "POST":
            return await self.handle_create_membership_order(request, current_user)
        
        # Property endpoints
        if path.startswith("/api/v1/properties/") and method == "GET":
            property_id = path.split("/")[-1]
            return self.handle_get_property_detail(property_id)
        
        # Scene endpoints - 这些直接传递给实际路由
        if path.startswith("/api/v1/scenes"):
            return None
        
        return None
    
    async def handle_login(self, request: Request):
        """处理登录"""
        try:
            body = await request.json()
            code = body.get("code")
            
            if not code:
                return self.create_response(
                    code=422,
                    message="缺少code参数",
                    status_code=422
                )
            
            if not code.strip():
                return self.create_response(
                    code=422,
                    message="code不能为空",
                    status_code=422
                )
            
            # 测试模式下返回固定用户
            user = self.test_users["user_001"]
            
            return self.create_response(
                data={
                    "token": "user_001",
                    "expiresIn": 7200,
                    "user": {
                        "id": user["id"],
                        "nickName": user["nickName"],
                        "avatarUrl": user["avatarUrl"]
                    }
                },
                status_code=201
            )
        except Exception as e:
            return self.create_response(
                code=1001,
                message=str(e),
                status_code=400
            )
    
    async def handle_phone_login(self, request: Request):
        """处理手机号登录"""
        try:
            body = await request.json()
            phone = body.get("phone")
            code = body.get("code")
            
            if not phone or not code:
                return self.create_response(
                    code=422,
                    message="缺少必要参数",
                    status_code=422
                )
            
            user = self.test_users["user_001"]
            
            return self.create_response(
                data={
                    "token": "user_001",
                    "expiresIn": 7200,
                    "user": {
                        "id": user["id"],
                        "nickName": user["nickName"],
                        "avatarUrl": user["avatarUrl"]
                    }
                },
                status_code=201
            )
        except Exception as e:
            return self.create_response(
                code=1002,
                message=str(e),
                status_code=400
            )
    
    async def handle_sms_code(self, request: Request):
        """处理发送短信验证码"""
        try:
            body = await request.json()
            phone = body.get("phone")
            
            if not phone:
                return self.create_response(
                    code=422,
                    message="缺少手机号",
                    status_code=422
                )
            
            return self.create_response(
                data={"sent": True},
                status_code=201
            )
        except Exception as e:
            return self.create_response(
                code=1003,
                message=str(e),
                status_code=400
            )
    
    def handle_validate_session(self, current_user):
        """验证会话"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        return self.create_response(
            data={
                "valid": True,
                "user": {
                    "id": current_user["id"],
                    "nickName": current_user["nickName"]
                }
            }
        )
    
    def handle_get_current_user(self, current_user):
        """获取当前用户信息"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        return self.create_response(
            data={
                "id": current_user["id"],
                "nickName": current_user["nickName"],
                "avatarUrl": current_user["avatarUrl"],
                "phone": current_user.get("phone"),
                "createdAt": current_user["createdAt"]
            }
        )
    
    async def handle_update_current_user(self, request: Request, current_user):
        """更新当前用户信息"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        try:
            body = await request.json()
            
            # 更新用户信息
            updated_user = current_user.copy()
            updated_user.update(body)
            
            return self.create_response(
                data={
                    "id": updated_user["id"],
                    "nickName": updated_user["nickName"],
                    "avatarUrl": updated_user["avatarUrl"],
                    "phone": updated_user.get("phone"),
                    "createdAt": updated_user["createdAt"]
                }
            )
        except Exception as e:
            return self.create_response(
                code=1002,
                message=f"更新失败: {str(e)}",
                status_code=400
            )
    
    def handle_get_user_by_id(self, user_id: str):
        """根据ID获取用户信息"""
        user = self.test_users.get(user_id)
        if not user:
            return self.create_response(
                code=404,
                message="用户不存在",
                status_code=404
            )
        
        return self.create_response(
            data={
                "id": user["id"],
                "nickname": user["nickName"],
                "avatar": user["avatarUrl"],
                "age": user["age"],
                "gender": "男" if user["gender"] == 1 else "女",
                "location": user["location"],
                "occupation": user["occupation"],
                "bio": user["bio"]
            }
        )
    
    def handle_get_user_stats(self, current_user):
        """获取用户统计信息"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        return self.create_response(
            data={
                "matchCount": 10,
                "messageCount": 50,
                "favoriteCount": 5
            }
        )
    
    def handle_get_profile(self, current_user):
        """获取个人资料"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        return self.create_response(
            data={
                "id": current_user["id"],
                "nickName": current_user["nickName"],
                "avatarUrl": current_user["avatarUrl"],
                "age": current_user["age"],
                "occupation": current_user["occupation"],
                "location": current_user["location"],
                "bio": current_user["bio"],
                "interests": current_user["interests"],
                "preferences": current_user["preferences"]
            }
        )
    
    async def handle_update_profile(self, request: Request, current_user):
        """更新个人资料"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        try:
            body = await request.json()
            
            # 更新资料
            updated_profile = current_user.copy()
            updated_profile.update(body)
            
            # 将更新后的数据保存到本地文件
            try:
                user_id = current_user["id"]
                test_user_data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "test_user_data.json")
                
                if os.path.exists(test_user_data_file):
                    with open(test_user_data_file, 'r', encoding='utf-8') as f:
                        user_data = json.load(f)
                    
                    # 更新用户数据
                    if user_id in user_data:
                        user_data[user_id].update(body)
                        
                        # 保存更新后的数据
                        with open(test_user_data_file, 'w', encoding='utf-8') as f:
                            json.dump(user_data, f, ensure_ascii=False, indent=2)
                        
                        print(f"Updated user data saved to {test_user_data_file}")
            except Exception as e:
                print(f"Warning: Could not save user data to file: {e}")
            
            return self.create_response(
                data=updated_profile
            )
        except Exception as e:
            return self.create_response(
                code=1002,
                message=f"更新失败: {str(e)}",
                status_code=400
            )
    
    async def handle_get_match_cards(self, request: Request, current_user):
        """获取匹配卡片"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        params = dict(request.query_params)
        match_type = params.get("matchType")
        user_role = params.get("userRole")
        
        if not match_type or not user_role:
            return self.create_response(
                code=422,
                message="缺少必要参数",
                status_code=422
            )
        
        # 对于匹配卡片，直接传递给实际路由处理，不在中间件中处理
        return None
    
    async def handle_match_action(self, request: Request, current_user):
        """处理匹配操作"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        try:
            body = await request.json()
            card_id = body.get("cardId")
            action = body.get("action")
            
            if not card_id or not action:
                return self.create_response(
                    code=422,
                    message="缺少必要参数",
                    status_code=422
                )
            
            # 模拟匹配结果
            is_match = action == "like"
            
            return self.create_response(
                data={
                    "isMatch": is_match,
                    "matchId": f"match_{card_id}" if is_match else None
                },
                status_code=201
            )
        except Exception as e:
            return self.create_response(
                code=500,
                message=f"操作失败: {str(e)}",
                status_code=500
            )
    
    async def handle_swipe_card(self, request: Request, current_user):
        """处理滑动卡片"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        try:
            body = await request.json()
            card_id = body.get("cardId")
            direction = body.get("direction")
            
            if not card_id or not direction:
                return self.create_response(
                    code=422,
                    message="缺少必要参数",
                    status_code=422
                )
            
            is_match = direction == "right"
            
            return self.create_response(
                data={"isMatch": is_match},
                status_code=201
            )
        except Exception as e:
            return self.create_response(
                code=500,
                message=f"操作失败: {str(e)}",
                status_code=500
            )
    
    async def handle_get_messages(self, request: Request, current_user):
        """获取消息列表"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        params = dict(request.query_params)
        match_id = params.get("matchId")
        
        if not match_id:
            return self.create_response(
                code=422,
                message="缺少matchId参数",
                status_code=422
            )
        
        # 返回测试消息数据
        messages = [
            {
                "id": "msg_001",
                "senderId": "user_002",
                "content": "你好！",
                "type": "text",
                "timestamp": "2024-01-01T10:00:00Z",
                "isRead": True
            },
            {
                "id": "msg_002",
                "senderId": current_user["id"],
                "content": "你好，很高兴认识你！",
                "type": "text",
                "timestamp": "2024-01-01T10:01:00Z",
                "isRead": True
            }
        ]
        
        return self.create_response(
            data={
                "messages": messages,
                "pagination": {
                    "page": int(params.get("page", 1)),
                    "limit": int(params.get("limit", 20)),
                    "total": len(messages)
                }
            }
        )
    
    async def handle_send_message(self, request: Request, current_user):
        """发送消息"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        try:
            body = await request.json()
            match_id = body.get("matchId")
            content = body.get("content")
            msg_type = body.get("type")
            
            if not match_id or not content or not msg_type:
                return self.create_response(
                    code=422,
                    message="缺少必要参数",
                    status_code=422
                )
            
            return self.create_response(
                data={
                    "id": f"msg_{int(time.time())}",
                    "timestamp": self.get_current_timestamp()
                },
                status_code=201
            )
        except Exception as e:
            return self.create_response(
                code=500,
                message=f"发送失败: {str(e)}",
                status_code=500
            )
    
    async def handle_mark_messages_read(self, request: Request, current_user):
        """标记消息已读"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        try:
            body = await request.json()
            match_id = body.get("matchId")
            
            if not match_id:
                return self.create_response(
                    code=422,
                    message="缺少matchId参数",
                    status_code=422
                )
            
            return self.create_response(
                data={"success": True}
            )
        except Exception as e:
            return self.create_response(
                code=500,
                message=f"操作失败: {str(e)}",
                status_code=500
            )
    
    async def handle_get_matches(self, request: Request, current_user):
        """获取匹配列表"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        params = dict(request.query_params)
        
        # 返回测试匹配数据
        matches = [
            {
                "id": "match_001",
                "user": {
                    "id": "user_002",
                    "name": "测试用户2",
                    "avatar": "https://picsum.photos/200/200?random=2"
                },
                "lastMessage": {
                    "content": "你好！",
                    "timestamp": "2024-01-01T10:00:00Z"
                },
                "unreadCount": 1
            }
        ]
        
        return self.create_response(
            data={
                "matches": matches,
                "pagination": {
                    "page": int(params.get("page", 1)),
                    "pageSize": int(params.get("pageSize", 10)),
                    "total": len(matches)
                }
            }
        )
    
    def handle_get_match_detail(self, match_id: str, current_user):
        """获取匹配详情"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        # 返回测试匹配详情
        return self.create_response(
            data={
                "id": match_id,
                "user": {
                    "id": "user_002",
                    "name": "测试用户2",
                    "avatar": "https://picsum.photos/200/200?random=2",
                    "age": 28,
                    "location": "上海",
                    "occupation": "设计师"
                },
                "matchedAt": "2024-01-01T00:00:00Z",
                "reason": "你们都喜欢旅行"
            }
        )
    
    async def handle_file_upload(self, request: Request, current_user):
        """处理文件上传"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        try:
            form = await request.form()
            file = form.get("file")
            file_type = form.get("type")
            
            if not file:
                return self.create_response(
                    code=400,
                    message="请选择文件",
                    status_code=400
                )
            
            if not file.content_type.startswith("image/"):
                return self.create_response(
                    code=400,
                    message="请上传图片文件",
                    status_code=400
                )
            
            # 返回测试文件URL
            return self.create_response(
                data={
                    "url": f"https://cdn.example.com/files/{file.filename}",
                    "filename": file.filename,
                    "size": 1024000,
                    "type": file.content_type
                },
                status_code=201
            )
        except Exception as e:
            return self.create_response(
                code=500,
                message=f"文件上传失败: {str(e)}",
                status_code=500
            )
    
    def handle_get_membership(self, current_user):
        """获取会员信息"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        return self.create_response(
            data={
                "level": "premium",
                "levelName": "高级会员",
                "expireDate": "2024-12-31T23:59:59Z",
                "features": ["无限滑动", "超级喜欢", "查看喜欢我的人"],
                "remainingSwipes": -1,
                "totalSwipes": -1
            }
        )
    
    async def handle_create_membership_order(self, request: Request, current_user):
        """创建会员订单"""
        if not current_user:
            return self.create_response(
                code=401,
                message="未授权访问",
                status_code=401
            )
        
        try:
            body = await request.json()
            plan_id = body.get("planId")
            
            if not plan_id:
                return self.create_response(
                    code=422,
                    message="缺少planId参数",
                    status_code=422
                )
            
            return self.create_response(
                data={
                    "orderId": f"order_{int(time.time())}",
                    "amount": 30.00,
                    "status": "pending",
                    "paymentUrl": "https://pay.example.com/order_123"
                },
                status_code=201
            )
        except Exception as e:
            return self.create_response(
                code=500,
                message=f"创建订单失败: {str(e)}",
                status_code=500
            )
    
    def handle_get_property_detail(self, property_id: str):
        """获取房源详情"""
        # 返回测试房源数据
        return self.create_response(
            data={
                "id": property_id,
                "type": "housing",
                "title": "精装两居室",
                "description": "房源描述",
                "price": 3000,
                "location": "朝阳区",
                "area": 80,
                "rooms": 2,
                "floor": "10/20",
                "orientation": "南北通透",
                "decoration": "精装修",
                "images": ["https://picsum.photos/400/300?random=1"],
                "landlord": {
                    "name": "房东姓名",
                    "avatar": "https://picsum.photos/200/200?random=landlord",
                    "phone": "13800138000"
                },
                "facilities": ["空调", "洗衣机", "冰箱"],
                "tags": ["近地铁", "拎包入住"],
                "publishTime": "2024-01-01T00:00:00Z"
            }
        )


def register_restful_test_middleware(app):
    """注册 RESTful 测试中间件"""
    app.add_middleware(RESTfulTestModeMiddleware)
    print("RESTful test mode middleware registered.")
