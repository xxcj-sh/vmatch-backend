#!/usr/bin/env python3
"""
生成有效测试数据的脚本
确保所有房源卡片中的房东ID都对应到有效的测试用户
"""

import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.test_data_generator import TestDataGenerator

def generate_valid_test_data():
    """生成有效的测试数据"""
    print("=== 生成有效的测试数据 ===\n")
    
    # 定义测试用户ID
    test_user_ids = ["user_001", "user_002", "user_003", "user_004", "user_005"]
    
    # 生成测试用户
    test_users = []
    for user_id in test_user_ids:
        user = TestDataGenerator.generate_user(user_id)
        test_users.append(user)
    
    print(f"已生成 {len(test_users)} 个测试用户")
    
    # 生成房源卡片，确保房东ID对应测试用户
    housing_cards = []
    for i in range(5):
        # 随机选择一个测试用户作为房东
        landlord_user_id = test_user_ids[i % len(test_user_ids)]
        
        card = TestDataGenerator.generate_card(
            card_id=f"housing_card_{i+1:03d}",
            match_type="housing", 
            user_role="seeker",
            landlord_user_id=landlord_user_id
        )
        
        # 验证房东ID是否正确
        assert card["landlordInfo"]["id"] == landlord_user_id, \
            f"房东ID不匹配: 期望 {landlord_user_id}, 实际 {card['landlordInfo']['id']}"
        
        housing_cards.append(card)
    
    print(f"已生成 {len(housing_cards)} 个房源卡片")
    
    # 生成匹配数据
    matches = []
    for i, card in enumerate(housing_cards):
        match = TestDataGenerator.generate_match(
            match_id=f"match_{i+1:03d}",
            user_id=f"test_seeker_{i+1:03d}",
            card_id=card["id"]
        )
        matches.append(match)
    
    print(f"已生成 {len(matches)} 个匹配记录")
    
    # 生成完整测试数据集
    test_data = {
        "metadata": {
            "generated_at": "2024-01-01 00:00:00",
            "description": "测试数据，确保房东ID与测试用户关联",
            "version": "1.0"
        },
        "users": test_users,
        "housing_cards": housing_cards,
        "matches": matches,
        "api_test_info": {
            "user_profile_endpoint": "/api/v1/user/profile",
            "valid_user_ids": test_user_ids,
            "test_urls": [
                f"http://localhost:8000/api/v1/user/profile?userId={user_id}"
                for user_id in test_user_ids
            ]
        }
    }
    
    # 保存测试数据
    output_file = "valid_test_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n测试数据已保存到: {output_file}")
    
    # 显示摘要信息
    print("\n=== 数据摘要 ===")
    print(f"测试用户: {len(test_users)} 个")
    print(f"房源卡片: {len(housing_cards)} 个")
    print(f"匹配记录: {len(matches)} 个")
    
    print("\n=== 测试用户列表 ===")
    for user in test_users:
        print(f"  - {user['id']}: {user['nickName']} ({user['occupation']})")
    
    print("\n=== 房源卡片房东信息 ===")
    for card in housing_cards:
        landlord = card["landlordInfo"]
        print(f"  - 卡片 {card['id']}: 房东ID={landlord['id']}, 姓名={landlord['name']}")
    
    print("\n=== API测试URL ===")
    for user_id in test_user_ids:
        print(f"  - http://localhost:8000/api/v1/user/profile?userId={user_id}")
    
    return test_data

if __name__ == "__main__":
    generate_valid_test_data()
    print("\n🎉 测试数据生成完成！所有房东ID都已正确映射到测试用户。")