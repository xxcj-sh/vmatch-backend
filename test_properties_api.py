#!/usr/bin/env python3
"""
测试新的properties API端点
"""

import requests
import json

def test_properties_api():
    """测试properties API"""
    
    # 测试URL
    base_url = "http://localhost:8000/api/v1"
    
    # 测试卡片ID
    test_card_id = "test_card"
    
    print("🧪 测试Properties API")
    print("=" * 50)
    
    # 1. 测试获取卡片列表
    print("1. 测试获取房源卡片列表...")
    try:
        response = requests.get(
            f"{base_url}/match/cards",
            params={
                "matchType": "housing",
                "userRole": "seeker",
                "page": 1,
                "pageSize": 5
            },
            headers={"Authorization": "Bearer user_001"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功获取卡片列表，共 {len(data.get('data', {}).get('list', []))} 个卡片")
            if data.get('data', {}).get('list'):
                first_card = data['data']['list'][0]
                print(f"   第一个卡片ID: {first_card.get('id')}")
                test_card_id = first_card.get('id')
        else:
            print(f"❌ 获取卡片列表失败: {response.status_code}")
            print(f"   响应: {response.text}")
    except Exception as e:
        print(f"❌ 获取卡片列表异常: {e}")
    
    print()
    
    # 2. 测试新的properties API
    print(f"2. 测试获取卡片详情: {test_card_id}...")
    try:
        response = requests.get(
            f"{base_url}/properties/{test_card_id}",
            headers={"Authorization": "Bearer user_001"}
        )
        
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                print("✅ Properties API测试成功！")
            else:
                print(f"❌ API返回错误: {data.get('message')}")
        else:
            print(f"❌ API请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Properties API测试异常: {e}")
    
    print()
    
    # 3. 测试不存在的卡片
    print("3. 测试不存在的卡片...")
    try:
        response = requests.get(
            f"{base_url}/properties/non_existent_card",
            headers={"Authorization": "Bearer user_001"}
        )
        
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 1404:
                print("✅ 404错误处理正常")
            else:
                print(f"❌ 意外的响应码: {data.get('code')}")
        else:
            print(f"❌ 意外的状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    test_properties_api()