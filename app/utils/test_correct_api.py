#!/usr/bin/env python3
"""
测试正确的API端点
"""

import requests
import json

# 测试本地API端点
BASE_URL = "http://localhost:8000/api/v1"

def test_api_endpoints():
    print("=== 测试正确的API端点 ===\n")
    
    # 1. 测试获取匹配卡片
    print("1. 测试获取匹配卡片...")
    try:
        response = requests.get(f"{BASE_URL}/match/cards", params={
            "matchType": "housing",
            "userRole": "seeker",
            "page": 1,
            "pageSize": 5
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ /api/v1/match/cards 成功 - 状态码: {response.status_code}")
            if data.get("code") == 0:
                cards = data.get("data", {}).get("cards", [])
                print(f"   返回卡片数量: {len(cards)}")
                if cards:
                    print(f"   示例卡片ID: {cards[0]['id']}")
                    print(f"   房东信息: {cards[0].get('landlordInfo', {}).get('id', 'N/A')}")
            else:
                print(f"   错误信息: {data.get('message')}")
        else:
            print(f"❌ /api/v1/match/cards 失败 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 连接错误: {e}")
    
    # 2. 测试用户资料API
    print("\n2. 测试用户资料API...")
    test_user_ids = ["user_001", "user_002", "user_003"]
    
    for user_id in test_user_ids:
        try:
            response = requests.get(f"{BASE_URL}/user/profile", params={"userId": user_id})
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    user_data = data.get("data", {})
                    print(f"✅ 用户 {user_id}: {user_data.get('nickName', '未知')} - 有效")
                else:
                    print(f"⚠️ 用户 {user_id}: {data.get('message', '未知错误')}")
            else:
                print(f"❌ 用户 {user_id}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ 用户 {user_id}: 连接错误 {e}")
    
    # 3. 测试匹配详情API
    print("\n3. 测试匹配详情API...")
    try:
        # 先获取一些匹配卡片
        cards_response = requests.get(f"{BASE_URL}/match/cards", params={
            "matchType": "housing",
            "userRole": "seeker",
            "page": 1,
            "pageSize": 1
        })
        
        if cards_response.status_code == 200:
            cards_data = cards_response.json()
            if cards_data.get("code") == 0 and cards_data.get("data", {}).get("cards"):
                card = cards_data["data"]["cards"][0]
                card_id = card["id"]
                
                # 创建一个匹配
                match_response = requests.post(f"{BASE_URL}/match/action", json={
                    "cardId": card_id,
                    "action": "like",
                    "matchType": "housing"
                })
                
                if match_response.status_code == 200:
                    match_data = match_response.json()
                    if match_data.get("code") == 0:
                        match_id = match_data.get("data", {}).get("matchId")
                        if match_id:
                            # 测试匹配详情
                            detail_response = requests.get(f"{BASE_URL}/match/detail/{match_id}")
                            if detail_response.status_code == 200:
                                print(f"✅ /api/v1/match/detail/{match_id} - 成功")
                            else:
                                print(f"❌ /api/v1/match/detail/{match_id} - 状态码: {detail_response.status_code}")
    except Exception as e:
        print(f"❌ 匹配详情测试错误: {e}")
    
    print("\n=== 正确的API端点总结 ===")
    print("获取房源卡片: GET /api/v1/match/cards")
    print("参数: matchType=housing&userRole=seeker&page=1&pageSize=5")
    print("用户资料: GET /api/v1/user/profile?userId={user_id}")
    print("匹配详情: GET /api/v1/match/detail/{matchId}")

if __name__ == "__main__":
    test_api_endpoints()