#!/usr/bin/env python3
"""
测试用户角色资料API
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    # 模拟认证头（根据实际项目的认证方式调整）
    headers = {
        "Authorization": "Bearer test_token_001",
        "Content-Type": "application/json"
    }
    
    print("🧪 测试用户角色资料API")
    print("=" * 50)
    
    # 测试获取所有角色资料
    print("\n1. 测试 GET /users/me/profiles")
    try:
        response = requests.get(f"{BASE_URL}/users/me/profiles", headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功获取数据")
            print(f"用户ID: {data.get('user_id')}")
            print(f"总资料数: {data.get('total_count')}")
            print(f"激活资料数: {data.get('active_count')}")
            
            # 显示按场景分组的资料
            for scene in data.get('by_scene', []):
                print(f"📂 {scene['scene_type']} 场景: {len(scene['profiles'])} 个资料")
                for profile in scene['profiles']:
                    print(f"  - {profile['role_type']}: {profile['display_name']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    # 测试获取特定场景的资料
    print("\n2. 测试 GET /users/me/profiles/housing")
    try:
        response = requests.get(f"{BASE_URL}/users/me/profiles/housing", headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                profiles = data.get('data', {}).get('profiles', [])
                print(f"✅ 找到 {len(profiles)} 个 housing 场景资料")
                for profile in profiles:
                    print(f"  - {profile['role_type']}: {profile['display_name']}")
            else:
                print(f"❌ API返回错误: {data.get('message')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    # 测试获取特定角色资料
    print("\n3. 测试 GET /users/me/profiles/housing/housing_seeker")
    try:
        response = requests.get(f"{BASE_URL}/users/me/profiles/housing/housing_seeker", headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                profile = data.get('data')
                print(f"✅ 成功获取 housing_seeker 资料")
                print(f"  显示名称: {profile['display_name']}")
                print(f"  简介: {profile['bio']}")
                
                # 解析 profile_data
                if profile.get('profile_data'):
                    profile_data = json.loads(profile['profile_data']) if isinstance(profile['profile_data'], str) else profile['profile_data']
                    print(f"  预算范围: {profile_data.get('budget_range')}")
                    print(f"  偏好区域: {profile_data.get('preferred_areas')}")
            else:
                print(f"❌ API返回错误: {data.get('message')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API测试完成！")

if __name__ == "__main__":
    test_api()