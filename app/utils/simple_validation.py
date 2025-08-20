#!/usr/bin/env python3
"""
简化验证脚本：验证房东ID与用户ID映射关系
"""

import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.test_data_generator import TestDataGenerator

def validate_landlord_mapping():
    """验证房东ID与用户ID映射关系"""
    print("=== 验证房东ID与用户ID映射关系 ===\n")
    
    # 生成测试用户
    test_users = []
    valid_user_ids = ["user_001", "user_002", "user_003", "user_004", "user_005"]
    
    for user_id in valid_user_ids:
        user = TestDataGenerator.generate_user(user_id)
        test_users.append(user)
    
    # 生成房源卡片
    housing_cards = []
    for i in range(10):
        card = TestDataGenerator.generate_card(
            card_id=f"housing_card_{i+1}",
            match_type="housing", 
            user_role="seeker"
        )
        housing_cards.append(card)
    
    # 验证映射关系
    print("预定义测试用户:")
    for user in test_users:
        print(f"  - {user['id']}: {user['nickName']} ({user['occupation']})")
    
    print(f"\n生成房源卡片数量: {len(housing_cards)}")
    
    valid_mappings = 0
    invalid_mappings = 0
    
    print("\n房东ID映射验证:")
    for card in housing_cards:
        landlord_id = card["landlordInfo"]["id"]
        landlord_name = card["landlordInfo"]["name"]
        
        is_valid = landlord_id in valid_user_ids
        
        if is_valid:
            valid_mappings += 1
            status = "✅ 有效"
        else:
            invalid_mappings += 1
            status = "❌ 无效"
        
        print(f"  - 卡片 {card['id']}: 房东ID={landlord_id}, 姓名={landlord_name} {status}")
    
    print(f"\n验证结果:")
    print(f"  - 有效映射: {valid_mappings}")
    print(f"  - 无效映射: {invalid_mappings}")
    print(f"  - 成功率: {(valid_mappings/len(housing_cards))*100:.1f}%")
    
    # 保存验证结果
    validation_result = {
        "test_users": test_users,
        "housing_cards": housing_cards,
        "validation": {
            "valid_user_ids": valid_user_ids,
            "mapping_summary": {
                "total_cards": len(housing_cards),
                "valid_mappings": valid_mappings,
                "invalid_mappings": invalid_mappings,
                "success_rate": f"{(valid_mappings/len(housing_cards))*100:.1f}%"
            }
        }
    }
    
    with open("landlord_mapping_validation.json", "w", encoding="utf-8") as f:
        json.dump(validation_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n验证结果已保存到 landlord_mapping_validation.json")
    
    # 生成可直接用于测试的数据文件
    test_data = {
        "users": test_users,
        "housing_cards": housing_cards,
        "api_endpoints": {
            "user_profile": "/api/v1/user/profile",
            "expected_valid_user_ids": valid_user_ids
        }
    }
    
    with open("test_data_with_valid_mappings.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"测试数据已保存到 test_data_with_valid_mappings.json")
    
    return valid_mappings == len(housing_cards)

if __name__ == "__main__":
    success = validate_landlord_mapping()
    if success:
        print("\n🎉 所有房东ID都已正确映射到测试用户！")
    else:
        print("\n⚠️ 存在未正确映射的房东ID，请检查配置")