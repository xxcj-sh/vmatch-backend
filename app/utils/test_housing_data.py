#!/usr/bin/env python3
"""
测试房源数据生成器
用于验证 matchType: "housing", userRole: "seeker" 场景下的数据生成
"""
import json
from app.utils.test_data_generator import TestDataGenerator

def test_housing_data():
    """测试房源数据生成"""
    print("=== 测试房源数据生成 ===\n")
    
    # 测试房源信息生成
    print("1. 测试房源信息生成:")
    house_info = TestDataGenerator.generate_house_info()
    print(json.dumps(house_info, indent=2, ensure_ascii=False))
    
    # 测试房东信息生成
    print("\n2. 测试房东信息生成:")
    landlord_info = TestDataGenerator.generate_landlord_info()
    print(json.dumps(landlord_info, indent=2, ensure_ascii=False))
    
    # 测试租客信息生成
    print("\n3. 测试租客信息生成:")
    tenant_info = TestDataGenerator.generate_tenant_info()
    print(json.dumps(tenant_info, indent=2, ensure_ascii=False))
    
    # 测试房源卡片生成（租客视角）
    print("\n4. 测试房源卡片生成（租客视角，matchType=housing, userRole=seeker）:")
    housing_card_seeker = TestDataGenerator.generate_card(
        match_type="housing", 
        user_role="seeker"
    )
    print(json.dumps(housing_card_seeker, indent=2, ensure_ascii=False))
    
    # 测试租客卡片生成（房东视角）
    print("\n5. 测试租客卡片生成（房东视角，matchType=housing, userRole=provider）:")
    housing_card_provider = TestDataGenerator.generate_card(
        match_type="housing", 
        user_role="provider"
    )
    print(json.dumps(housing_card_provider, indent=2, ensure_ascii=False))
    
    # 测试API响应
    print("\n6. 测试API响应（matchType=housing, userRole=seeker）:")
    api_response = TestDataGenerator.generate_match_cards_response(
        count=3, 
        match_type="housing", 
        user_role="seeker"
    )
    print(json.dumps(api_response, indent=2, ensure_ascii=False))
    
    # 验证数据结构
    print("\n7. 验证数据结构完整性:")
    data = api_response["data"]["list"][0]
    
    # 检查必需字段
    required_fields = ["id", "name", "avatar", "occupation", "matchType", "userRole"]
    for field in required_fields:
        if field in data:
            print(f"✓ {field}: 存在")
        else:
            print(f"✗ {field}: 缺失")
    
    # 检查房源相关字段（租客视角）
    if data.get("userRole") == "seeker":
        housing_fields = ["houseInfo", "landlordInfo"]
        for field in housing_fields:
            if field in data:
                print(f"✓ {field}: 存在")
            else:
                print(f"✗ {field}: 缺失")
    
    # 检查租客相关字段（房东视角）
    if data.get("userRole") == "provider":
        tenant_field = "tenantInfo"
        if tenant_field in data:
            print(f"✓ {tenant_field}: 存在")
        else:
            print(f"✗ {tenant_field}: 缺失")

if __name__ == "__main__":
    test_housing_data()