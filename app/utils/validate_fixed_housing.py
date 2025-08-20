#!/usr/bin/env python3
"""
验证固定测试房源ID的可用性
确保每个房源ID都能正确对应到测试样本
"""

import json
import os

def validate_fixed_housing_data():
    """验证固定房源数据的完整性"""
    
    # 读取固定测试数据
    with open('fixed_housing_test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("🔍 验证固定房源数据完整性...")
    
    # 验证房源ID与卡片ID的映射
    housing_to_card = {}
    card_to_housing = {}
    
    for card in data['housingCards']:
        card_id = card['id']
        house_id = card['houseInfo']['id']
        landlord_id = card['landlordInfo']['id']
        
        housing_to_card[house_id] = card_id
        card_to_housing[card_id] = house_id
        
        print(f"✅ 房源ID: {house_id} -> 卡片ID: {card_id} -> 房东ID: {landlord_id}")
    
    # 验证房东用户存在
    landlord_ids = [user['id'] for user in data['testUsers']]
    print(f"\n👥 测试房东用户: {landlord_ids}")
    
    # 检查每个房源的房东是否在用户列表中
    for card in data['housingCards']:
        landlord_id = card['landlordInfo']['id']
        if landlord_id in landlord_ids:
            print(f"✅ 房东 {landlord_id} 存在")
        else:
            print(f"❌ 房东 {landlord_id} 不存在")
    
    # 生成测试URL
    print(f"\n🔗 测试API端点:")
    for card in data['housingCards']:
        card_id = card['id']
        house_id = card['houseInfo']['id']
        landlord_id = card['landlordInfo']['id']
        
        print(f"\n🏠 房源: {house_id}")
        print(f"   获取房源卡片: GET /api/v1/match/cards?matchType=housing&userRole=seeker")
        print(f"   获取卡片详情: GET /api/v1/match/detail/{card_id}")
        print(f"   获取房东信息: GET /api/v1/user/profile?userId={landlord_id}")
    
    # 验证数据完整性
    expected_houses = ["house_test_001", "house_test_002", "house_test_003", 
                      "house_test_004", "house_test_005"]
    
    actual_houses = list(housing_to_card.keys())
    
    if set(expected_houses) == set(actual_houses):
        print(f"\n✅ 房源ID验证通过: 所有预期房源ID都存在")
    else:
        print(f"\n❌ 房源ID验证失败")
        print(f"   预期: {expected_houses}")
        print(f"   实际: {actual_houses}")
    
    return {
        "housing_to_card": housing_to_card,
        "card_to_housing": card_to_housing,
        "total_cards": len(data['housingCards']),
        "total_users": len(data['testUsers']),
        "validation_passed": set(expected_houses) == set(actual_houses)
    }

def generate_api_test_urls():
    """生成API测试URL"""
    
    with open('fixed_housing_test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n📋 API测试命令:")
    print("# 启动服务后，使用以下命令测试:")
    print()
    
    # 获取房源卡片
    print("# 1. 获取所有房源卡片")
    print('curl "http://localhost:8000/api/v1/match/cards?matchType=housing&userRole=seeker&page=1&pageSize=10"')
    print()
    
    # 测试每个房源
    for card in data['housingCards']:
        card_id = card['id']
        house_id = card['houseInfo']['id']
        landlord_id = card['landlordInfo']['id']
        
        print(f"# 房源: {house_id}")
        print(f'curl "http://localhost:8000/api/v1/user/profile?userId={landlord_id}"')
        print()

if __name__ == "__main__":
    validation_result = validate_fixed_housing_data()
    generate_api_test_urls()
    
    if validation_result['validation_passed']:
        print("🎉 所有验证通过！固定房源ID已正确对应到测试样本")
    else:
        print("⚠️  验证失败，请检查数据生成逻辑")