#!/usr/bin/env python3
"""
测试API房源数据接口
验证通过API调用 matchType: "housing", userRole: "seeker" 返回正确的房源数据
"""
import json
from app.utils.test_data_generator import TestDataGenerator

def test_api_housing_response():
    """测试API房源数据响应"""
    print("=== 测试API房源数据响应 ===\n")
    
    # 模拟API请求参数
    params = {
        "matchType": "housing",
        "userRole": "seeker",
        "pageSize": 5
    }
    
    # 测试API响应
    print("1. 测试API响应（/api/v1/match/cards）:")
    response = TestDataGenerator.mock_api_response(
        api_path="/api/v1/match/cards",
        method="GET",
        params=params
    )
    
    print("响应状态:", "成功" if response["code"] == 0 else "失败")
    print("响应消息:", response["message"])
    
    if response["code"] == 0:
        data = response["data"]
        print(f"总数量: {data['total']}")
        print(f"当前页: {data['page']}")
        print(f"每页数量: {data['pageSize']}")
        
        print("\n房源列表:")
        for i, card in enumerate(data["list"], 1):
            print(f"\n--- 房源 {i} ---")
            print(f"房源ID: {card['id']}")
            print(f"房东姓名: {card['name']}")
            print(f"距离: {card['distance']}")
            print(f"匹配类型: {card['matchType']}")
            print(f"用户角色: {card['userRole']}")
            
            # 房源信息
            if "houseInfo" in card:
                house = card["houseInfo"]
                print(f"房源标题: {house['title']}")
                print(f"租金: ¥{house['price']}/月")
                print(f"面积: {house['area']}㎡")
                print(f"朝向: {house['orientation']}")
                print(f"楼层: {house['floor']}")
                print(f"装修: {house['decoration']}")
                print(f"小区: {house['community']}")
                print(f"位置: {house['location']}")
                print(f"特色: {', '.join(house['features'])}")
                
            # 房东信息
            if "landlordInfo" in card:
                landlord = card["landlordInfo"]
                print(f"房东职业: {landlord['occupation']}")
                print(f"响应率: {landlord['responseRate']}")
                print(f"是否认证: {'是' if landlord['verified'] else '否'}")
    
    # 测试不同用户角色
    print("\n" + "="*50)
    print("2. 测试房东视角（userRole=provider）:")
    
    params_provider = {
        "matchType": "housing",
        "userRole": "provider",
        "pageSize": 2
    }
    
    response_provider = TestDataGenerator.mock_api_response(
        api_path="/api/v1/match/cards",
        method="GET",
        params=params_provider
    )
    
    if response_provider["code"] == 0:
        data = response_provider["data"]
        print("租客列表:")
        for i, card in enumerate(data["list"], 1):
            print(f"\n--- 租客 {i} ---")
            print(f"租客姓名: {card['name']}")
            print(f"职业: {card['occupation']}")
            print(f"预算: ¥{card['tenantInfo']['budget']}/月")
            print(f"期望房型: {card['tenantInfo']['roomType']}")
            print(f"期望区域: {', '.join(card['tenantInfo']['preferredAreas'])}")
            print(f"入住时间: {card['tenantInfo']['moveInDate']}")

if __name__ == "__main__":
    test_api_housing_response()