#!/usr/bin/env python3
"""
验证房源数据生成
确认 matchType: "housing", userRole: "seeker" 场景下的测试数据正确返回房源数据
"""
import json
from app.utils.test_data_generator import TestDataGenerator

def validate_housing_data():
    """验证房源数据"""
    print("✅ 验证 matchType: 'housing', userRole: 'seeker' 场景")
    print("=" * 60)
    
    # 直接测试API响应
    response = TestDataGenerator.mock_api_response(
        api_path="/api/v1/match/cards",
        method="GET",
        params={
            "matchType": "housing",
            "userRole": "seeker",
            "pageSize": 1
        }
    )
    
    if response["code"] == 0:
        card = response["data"]["list"][0]
        
        # 验证匹配类型和用户角色
        assert card["matchType"] == "housing", f"匹配类型错误: {card['matchType']}"
        assert card["userRole"] == "seeker", f"用户角色错误: {card['userRole']}"
        
        # 验证房源信息
        assert "houseInfo" in card, "缺少房源信息"
        house = card["houseInfo"]
        required_house_fields = ["title", "price", "area", "location", "features"]
        for field in required_house_fields:
            assert field in house, f"房源信息缺少字段: {field}"
        
        # 验证房东信息
        assert "landlordInfo" in card, "缺少房东信息"
        landlord = card["landlordInfo"]
        required_landlord_fields = ["name", "occupation", "verified"]
        for field in required_landlord_fields:
            assert field in landlord, f"房东信息缺少字段: {field}"
        
        print("✅ 验证通过！")
        print(f"   匹配类型: {card['matchType']}")
        print(f"   用户角色: {card['userRole']}")
        print(f"   房源标题: {house['title']}")
        print(f"   租金: ¥{house['price']}/月")
        print(f"   面积: {house['area']}㎡")
        print(f"   位置: {house['location']}")
        print(f"   特色: {', '.join(house['features'])}")
        print(f"   房东: {landlord['name']} ({landlord['occupation']})")
        
        return True
    else:
        print("❌ API响应失败")
        return False

if __name__ == "__main__":
    success = validate_housing_data()
    if success:
        print("\n🎉 所有验证通过！房源数据生成器已正确配置")
    else:
        print("\n❌ 验证失败，请检查配置")