from typing import Dict, List, Any, Optional
import uuid
import time
import random

class MockDataService:
    """模拟数据服务"""
    
    def __init__(self):
        """初始化模拟数据"""
        self.users: Dict[str, Dict[str, Any]] = {}
        self.cards: Dict[str, Dict[str, Any]] = {}
        self.matches: Dict[str, Dict[str, Any]] = {}
        self.messages: Dict[str, List[Dict[str, Any]]] = {}
        self.sms_codes: Dict[str, Dict[str, Any]] = {}
        
        # 初始化一些测试数据
        self._init_test_data()
    
    def _init_test_data(self):
        """初始化测试数据"""
        # 创建测试用户
        test_user = self.create_user({
            "id": "user_001",  # 固定ID用于测试
            "nickName": "测试用户",
            "avatarUrl": "https://example.com/avatar1.jpg",
            "gender": 1,
            "age": 28,
            "occupation": "软件工程师",
            "location": "北京",
            "bio": "喜欢编程和旅行",
            "matchType": "dating",
            "userRole": "seeker",
            "interests": ["编程", "旅行", "音乐"],
            "preferences": {
                "ageRange": [25, 35],
                "distance": 10
            }
        })
        
        # 创建另一个测试用户（用于测试获取用户资料）
        self.create_user({
            "id": "card_001",  # 固定ID用于测试
            "nickName": "测试卡片用户",
            "avatarUrl": "https://example.com/avatar2.jpg",
            "gender": 2,
            "age": 26,
            "occupation": "设计师",
            "location": "上海",
            "bio": "喜欢设计和摄影",
            "matchType": "dating",
            "userRole": "provider",
            "interests": ["设计", "摄影", "旅行"],
            "preferences": {
                "ageRange": [25, 35],
                "distance": 15
            }
        })
        
        # 创建测试卡片
        for i in range(1, 11):
            card_id = f"card_00{i}"
            self.create_card({
                "id": card_id,
                "name": f"测试卡片{i}",
                "avatar": f"https://example.com/avatar{i}.jpg",
                "age": random.randint(25, 35),
                "occupation": random.choice(["软件工程师", "设计师", "产品经理", "市场专员"]),
                "distance": f"{random.randint(1, 15)}km",
                "interests": random.sample(["编程", "旅行", "音乐", "电影", "阅读", "摄影", "健身"], 3),
                "matchType": "dating",
                "bio": f"这是测试卡片{i}的个人简介"
            })
        
        # 创建测试匹配
        match = {
            "isMatch": True,
            "matchId": "match_001"
        }
        
        # 创建匹配记录
        self.matches["match_001"] = {
            "id": "match_001",
            "userId1": "user_001",
            "userId2": "card_001",
            "reason": "你们有共同的兴趣",
            "createTime": int(time.time()),
            "isRead": False,
            "type": "dating",
            "status": "matched"
        }
        
        # 创建测试消息
        self.messages["match_001"] = []
        self.send_message("match_001", "user_001", "你好，很高兴认识你！", "text")
        self.send_message("match_001", "card_001", "你好，我也很高兴认识你！", "text")
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        user_id = user_data.get("id") or str(uuid.uuid4())
        user = {
            "id": user_id,
            **user_data
        }
        self.users[user_id] = user
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取用户"""
        return self.users.get(user_id)
    
    def get_user_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        """根据token获取用户信息（测试模式）"""
        # 测试模式下，token就是用户ID
        # 支持测试用例中的token
        if token == "user_001":
            return self.users.get("user_001")
        elif token == "invalid_token":
            return None
        else:
            return self.users.get(token)
    
    def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户资料"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        user.update(profile_data)
        return user
    
    def create_card(self, card_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建卡片"""
        card_id = card_data.get("id") or str(uuid.uuid4())
        card = {
            "id": card_id,
            **card_data
        }
        self.cards[card_id] = card
        return card
    
    def get_cards(self, match_type: str, user_role: str, page: int, page_size: int) -> Dict[str, Any]:
        """获取匹配卡片"""
        filtered_cards = [
            card for card in self.cards.values()
            if card.get("matchType") == match_type
        ]
        
        start = (page - 1) * page_size
        end = start + page_size
        
        return {
            "total": len(filtered_cards),
            "list": filtered_cards[start:end],
            "page": page,
            "pageSize": page_size
        }
    
    def create_match(self, user_id: str, card_id: str, action: str) -> Dict[str, Any]:
        """创建匹配"""
        # 在实际应用中，需要检查用户是否已经对该卡片进行过操作
        
        # 模拟匹配逻辑
        is_match = action == "like" and random.random() > 0.5
        
        result = {
            "isMatch": is_match,
            "matchId": None
        }
        
        if is_match:
            match_id = str(uuid.uuid4())
            match = {
                "id": match_id,
                "userId1": user_id,
                "userId2": card_id,
                "reason": "你们有共同的兴趣",
                "createTime": int(time.time()),
                "isRead": False,
                "type": "dating",
                "status": "matched"
            }
            self.matches[match_id] = match
            result["matchId"] = match_id
            
            # 初始化消息列表
            self.messages[match_id] = []
        
        return result
    
    def get_matches(self, user_id: str, status: str, page: int, page_size: int) -> Dict[str, Any]:
        """获取匹配列表"""
        filtered_matches = []
        
        for match in self.matches.values():
            if match["userId1"] == user_id or match["userId2"] == user_id:
                if status == "all" or \
                   (status == "new" and not match["isRead"]) or \
                   (status == "contacted" and match["isRead"]):
                    # 添加卡片信息
                    other_user_id = match["userId2"] if match["userId1"] == user_id else match["userId1"]
                    card_info = self.cards.get(other_user_id, {}) or self.users.get(other_user_id, {})
                    match_with_card = {**match, "cardInfo": card_info}
                    filtered_matches.append(match_with_card)
        
        # 按创建时间排序
        filtered_matches.sort(key=lambda x: x["createTime"], reverse=True)
        
        start = (page - 1) * page_size
        end = start + page_size
        
        return {
            "total": len(filtered_matches),
            "list": filtered_matches[start:end],
            "page": page,
            "pageSize": page_size
        }
    
    def get_match_by_id(self, match_id: str, user_id: str = None) -> Optional[Dict[str, Any]]:
        """根据ID获取匹配"""
        match = self.matches.get(match_id)
        if not match:
            return None
        
        # 添加卡片信息
        if user_id:
            other_user_id = match["userId2"] if match["userId1"] == user_id else match["userId1"]
        else:
            other_user_id = match["userId2"]  # 默认返回第二个用户的信息
            
        card_info = self.cards.get(other_user_id, {}) or self.users.get(other_user_id, {})
        return {**match, "cardInfo": card_info}
    
    def get_chat_history(self, match_id: str, page: int, page_size: int) -> Dict[str, Any]:
        """获取聊天记录"""
        messages = self.messages.get(match_id, [])
        
        # 按时间排序
        messages.sort(key=lambda x: x["timestamp"], reverse=True)
        
        start = (page - 1) * page_size
        end = start + page_size
        
        return {
            "total": len(messages),
            "list": messages[start:end],
            "page": page,
            "pageSize": page_size
        }
    
    def send_message(self, match_id: str, sender_id: str, content: str, msg_type: str) -> Dict[str, Any]:
        """发送消息"""
        if match_id not in self.messages:
            self.messages[match_id] = []
        
        # 获取发送者信息
        sender = self.get_user_by_id(sender_id) or self.cards.get(sender_id, {})
        
        message = {
            "id": str(uuid.uuid4()),
            "content": content,
            "type": msg_type,
            "senderId": sender_id,
            "senderAvatar": sender.get("avatarUrl") or sender.get("avatar", ""),
            "senderName": sender.get("nickName") or sender.get("name", ""),
            "timestamp": int(time.time()),
            "isRead": False
        }
        
        self.messages[match_id].append(message)
        
        # 标记匹配为已读
        match = self.matches.get(match_id)
        if match:
            match["isRead"] = True
        
        return message
    
    def upload_file(self, file_type: str) -> Dict[str, Any]:
        """上传文件"""
        # 模拟文件上传
        file_id = str(uuid.uuid4())
        return {
            "url": f"https://example.com/uploads/{file_type}/{file_id}.jpg"
        }

mock_data_service = MockDataService()