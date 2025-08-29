#!/usr/bin/env python3
"""
测试用户角色资料API接口
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_user_profiles_api():
    """测试用户角色资料相关的API接口"""
    
    print("=== 测试用户角色资料API接口 ===\n")
    
    # 模拟用户认证 - 这里需要根据实际的认证方式调整
    headers = {
        "Content-Type": "application/json",
        # 注意：这里需要实际的认证token，暂时使用模拟数据
        "Authorization": "Bearer test_token_for_test_user_001"
    }
    
    # 1. 测试获取用户所有角色资料
    print("1. 测试获取用户所有角色资料")
    try:
        response = requests.get(f"{BASE_URL}/users/me/profiles", headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"用户ID: {data.get('user_id')}")
            print(f"总资料数: {data.get('total_count')}")
            print(f"激活资料数: {data.get('active_count')}")
            print("按场景分组的资料:")
            for scene in data.get('by_scene', []):
                print(f"  - {scene['scene_type']}: {len(scene['profiles'])} 个资料")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. 测试获取特定场景下的角色资料
    print("2. 测试获取housing场景下的角色资料")
    try:
        response = requests.get(f"{BASE_URL}/users/me/profiles/housing", headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                profiles = data.get('data', {}).get('profiles', [])
                print(f"housing场景下有 {len(profiles)} 个角色资料:")
                for profile in profiles:
                    print(f"  - {profile['role_type']}: {profile['display_name']}")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. 测试获取特定角色的资料
    print("3. 测试获取housing.housing_seeker角色资料")
    try:
        response = requests.get(f"{BASE_URL}/users/me/profiles/housing/housing_seeker", headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                profile = data.get('data')
                print(f"角色资料: {profile['display_name']}")
                print(f"简介: {profile['bio']}")
                print(f"标签: {profile.get('tags', [])}")
                
                # 解析profile_data
                if profile.get('profile_data'):
                    profile_data = json.loads(profile['profile_data']) if isinstance(profile['profile_data'], str) else profile['profile_data']
                    print(f"预算范围: {profile_data.get('budget_range')}")
                    print(f"偏好区域: {profile_data.get('preferred_areas')}")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 4. 测试获取dating场景下的角色资料
    print("4. 测试获取dating场景下的角色资料")
    try:
        response = requests.get(f"{BASE_URL}/users/me/profiles/dating", headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                profiles = data.get('data', {}).get('profiles', [])
                print(f"dating场景下有 {len(profiles)} 个角色资料:")
                for profile in profiles:
                    print(f"  - {profile['role_type']}: {profile['display_name']}")
                    if profile.get('profile_data'):
                        profile_data = json.loads(profile['profile_data']) if isinstance(profile['profile_data'], str) else profile['profile_data']
                        print(f"    年龄: {profile_data.get('age')}")
                        print(f"职业: {profile_data.get('occupation')}")
                        print(f"兴趣: {profile_data.get('hobbies', [])}")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 5. 测试获取activity场景下的角色资料
    print("5. 测试获取activity场景下的角色资料")
    try:
        response = requests.get(f"{BASE_URL}/users/me/profiles/activity", headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                profiles = data.get('data', {}).get('profiles', [])
                print(f"activity场景下有 {len(profiles)} 个角色资料:")
                for profile in profiles:
                    print(f"  - {profile['role_type']}: {profile['display_name']}")
                    if profile.get('profile_data'):
                        profile_data = json.loads(profile['profile_data']) if isinstance(profile['profile_data'], str) else profile['profile_data']
                        if profile['role_type'] == 'activity_organizer':
                            print(f"    组织经验: {profile_data.get('organizing_experience')}")
                            print(f"专长: {profile_data.get('specialties', [])}")
                        elif profile['role_type'] == 'activity_participant':
                            print(f"    兴趣: {profile_data.get('interests', [])}")
                            print(f"    可参与时间: {profile_data.get('availability', {})}")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_user_profiles_api()