#!/usr/bin/env python3
"""
验证房东ID与用户ID映射关系的脚本
确保测试数据中的房东ID能够对应到有效的用户
"""

import sys
import os
import json
import requests

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.test_data_generator import TestDataGenerator

def validate_landlord_mapping():
    """验证房东ID与用户ID映射关系"""
    print("=== 验证房东ID与用户ID映射关系 ===\n")
    
    # 生成测试用户
    test_users = []
    for i in range(1, 6):
        user = TestDataGenerator.generate_user(f"user_00{i}")
        test_users.append(user)
    
    # 生成房源卡片
    housing_cards = []
    for i in range(5):
        card = TestDataGenerator.generate_card(
            card_id=f"housing_card_{i+1}",
            match_type="housing", 
            user_role="seeker"
        )
        housing_cards.append(card)
    
    # 验证映射关系
    print("测试用户列表:")
    user_ids = [user["id"] for user in test_users]
    for user in test_users:
        print(f"  - {user['id']}: {user['nickName']} ({user['occupation']})")
    
    print("\n房源卡片房东信息:")
    for card in housing_cards:
        landlord_id = card["landlordInfo"]["id"]
        landlord_name = card["landlordInfo"]["name"]
        
        is_valid = landlord_id in user_ids
        status = "✅ 有效" if is_valid else "❌ 无效"
        
        print(f"  - 卡片 {card['id']}: 房东ID={landlord_id}, 姓名={landlord_name} {status}")
    
    # 保存验证结果
    validation_result = {
        "test_users": test_users,
        "housing_cards": housing_cards,
        "validation": {
            "user_ids": user_ids,
            "landlord_mappings": [
                {
                    "card_id": card["id"],
                    "landlord_id": card["landlordInfo"]["id"],
                    "landlord_name": card["landlordInfo"]["name"],
                    "is_valid": card["landlordInfo"]["id"] in user_ids
                }
                for card in housing_cards
            ]
        }
    }
    
    with open("landlord_mapping_validation.json", "w", encoding="utf-8") as f:
        json.dump(validation_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n验证结果已保存到 landlord_mapping_validation.json")
    
    # 测试API访问
    print("\n=== 测试API访问 ===")
    base_url = "http://localhost:8000/api/v1"
    
    for card in housing_cards:
        landlord_id = card["landlordInfo"]["id"]
        try:
            response = requests.get(f"{base_url}/user/profile", params={"userId": landlord_id})
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    user_data = data.get("data", {})
                    print(f"✅ 房东ID {landlord_id}: API返回有效数据 - {user_data.get('nickName', '未知')}")
                else:
                    print(f"⚠️ 房东ID {landlord_id}: API返回错误 - {data.get('message', '未知错误')}")
            else:
                print(f"❌ 房东ID {landlord_id}: API访问失败 - HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ 房东ID {landlord_id}: 网络错误 - {str(e)}")
    
    return True

if __name__ == "__main__":
    validate_landlord_mapping()