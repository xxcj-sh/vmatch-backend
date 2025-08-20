#!/usr/bin/env python3
"""
测试数据生成器 - 包含有效用户关联
确保房东ID能够对应到实际的用户ID，使 /api/v1/user/profile 可以返回有效数据
"""
import json
import sys
import os
import random

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.test_data_generator import TestDataGenerator

def generate_test_users():
    """生成测试用户列表"""
    return [
        {
            "id": "user_001",
            "nickName": "林晓燕",
            "avatarUrl": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop&crop=face",
            "gender": 2,
            "age": 32,
            "occupation": "房产投资顾问",
            "location": "北京",
            "education": "硕士",
            "bio": "专业房产顾问，在北京有多套优质房源。为人随和，好沟通，希望能为租客提供舒适的居住体验。",
            "interests": ["房产投资", "室内设计", "智能家居"],
            "verified": True,
            "role": "landlord"
        },
        {
            "id": "user_002", 
            "nickName": "王思远",
            "avatarUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face",
            "gender": 1,
            "age": 28,
            "occupation": "互联网产品经理",
            "location": "北京",
            "education": "本科",
            "bio": "字节跳动产品经理，热爱生活，注重品质。有多套房源，希望找到爱干净的租客。",
            "interests": ["产品设计", "摄影", "咖啡文化"],
            "verified": True,
            "role": "landlord"
        },
        {
            "id": "user_003",
            "nickName": "张雨晴",
            "avatarUrl": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop&crop=face",
            "gender": 2,
            "age": 30,
            "occupation": "UI设计师",
            "location": "北京",
            "education": "本科",
            "bio": "独立UI设计师，热爱艺术与设计，注重生活品质，希望与有趣的租客共享空间。",
            "interests": ["设计", "艺术", "旅行"],
            "verified": True,
            "role": "landlord"
        }
    ]

def generate_housing_cards_with_valid_landlords():
    """生成包含有效房东关联的房源卡片"""
    users = generate_test_users()
    
    # 选择房东用户
    landlord_users = [u for u in users if u.get("role") == "landlord"]
    
    housing_cards = []
    
    for landlord in landlord_users:
        # 生成房源信息
        house_info = TestDataGenerator.generate_house_info()
        
        # 使用房东的用户ID作为房东ID
        landlord_info = {
            "id": landlord["id"],
            "name": landlord["nickName"],
            "avatar": landlord["avatarUrl"],
            "occupation": landlord["occupation"],
            "verified": landlord["verified"],
            "responseRate": f"{random.randint(90, 99)}%",
            "joinDate": TestDataGenerator.random_timestamp(1095),
            "bio": landlord["bio"]
        }
        
        card = {
            "id": f"housing_card_{landlord['id']}",
            "name": landlord["nickName"],
            "avatar": landlord["avatarUrl"],
            "gender": landlord["gender"],
            "age": landlord["age"],
            "occupation": landlord["occupation"],
            "location": landlord["location"],
            "distance": f"{random.uniform(0.1, 5.0):.1f}km",
            "bio": landlord["bio"],
            "education": landlord["education"],
            "interests": landlord["interests"],
            "matchType": "housing",
            "userRole": "seeker",
            "houseInfo": house_info,
            "landlordInfo": landlord_info
        }
        
        housing_cards.append(card)
    
    return housing_cards

def test_user_profile_api():
    """测试用户资料API是否能返回有效数据"""
    print("=== 测试用户资料API ===")
    
    # 生成测试用户
    test_users = generate_test_users()
    
    for user in test_users:
        user_id = user["id"]
        
        # 生成用户资料响应
        profile_response = TestDataGenerator.generate_user_profile_response(user_id)
        
        print(f"\n用户ID: {user_id}")
        print(f"昵称: {user['nickName']}")
        print(f"职业: {user['occupation']}")
        print(f"API响应: {json.dumps(profile_response, indent=2, ensure_ascii=False)}")
        
        # 验证数据有效性
        if profile_response.get("code") == 0 and profile_response.get("data"):
            print("✅ 用户资料API返回有效数据")
        else:
            print("❌ 用户资料API返回无效数据")

def test_housing_cards():
    """测试房源卡片数据"""
    print("\n=== 测试房源卡片数据 ===")
    
    cards = generate_housing_cards_with_valid_landlords()
    
    for i, card in enumerate(cards, 1):
        print(f"\n卡片 {i}:")
        print(f"卡片ID: {card['id']}")
        print(f"房东ID: {card['landlordInfo']['id']}")
        print(f"房东姓名: {card['landlordInfo']['name']}")
        print(f"房源标题: {card['houseInfo']['title']}")
        print(f"租金: ¥{card['houseInfo']['price']}/月")
        
        # 验证房东ID是否对应有效用户
        landlord_profile = TestDataGenerator.generate_user_profile_response(card['landlordInfo']['id'])
        if landlord_profile.get("code") == 0:
            print("✅ 房东ID有效，可获取用户资料")
        else:
            print("❌ 房东ID无效")

if __name__ == "__main__":
    # 运行测试
    test_user_profile_api()
    test_housing_cards()
    
    # 保存测试数据到文件
    test_data = {
        "test_users": generate_test_users(),
        "housing_cards": generate_housing_cards_with_valid_landlords()
    }
    
    with open("test_data_with_valid_users.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print("\n🎉 测试数据已保存到 test_data_with_valid_users.json")