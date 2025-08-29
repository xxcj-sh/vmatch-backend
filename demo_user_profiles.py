#!/usr/bin/env python3
"""
用户角色资料系统演示脚本
展示 test_user_001 用户的各种角色资料
"""

import json

def demo_user_profiles():
    """演示用户角色资料系统"""
    
    print("🎭 用户角色资料系统演示")
    print("=" * 60)
    print()
    
    # 模拟从API获取的用户资料数据
    user_profiles = {
        "user_id": "test_user_001",
        "total_count": 5,
        "active_count": 5,
        "profiles": [
            {
                "id": "profile_housing_seeker_001",
                "scene_type": "housing",
                "role_type": "housing_seeker",
                "display_name": "小李找房",
                "bio": "刚毕业的程序员，寻找合适的合租房源，希望找到志同道合的室友",
                "profile_data": {
                    "budget_range": [2000, 3500],
                    "preferred_areas": ["朝阳区", "海淀区", "昌平区"],
                    "room_type": "single_room",
                    "occupation": "软件工程师",
                    "company_location": "中关村"
                },
                "tags": ["程序员", "安静", "整洁", "不吸烟", "无宠物", "朝九晚六"]
            },
            {
                "id": "profile_housing_provider_001",
                "scene_type": "housing",
                "role_type": "housing_provider",
                "display_name": "李房东",
                "bio": "有多套优质房源出租，环境优美，交通便利，欢迎咨询",
                "profile_data": {
                    "properties": [
                        {
                            "address": "北京市朝阳区望京SOHO",
                            "rent": 3200,
                            "room_type": "2室1厅",
                            "area": 85,
                            "facilities": ["空调", "洗衣机", "冰箱", "WiFi", "电梯"]
                        }
                    ],
                    "landlord_type": "individual",
                    "response_time": "within_2_hours"
                },
                "tags": ["个人房东", "房源优质", "交通便利", "响应及时", "可看房"]
            },
            {
                "id": "profile_dating_seeker_001",
                "scene_type": "dating",
                "role_type": "dating_seeker",
                "display_name": "阳光小李",
                "bio": "热爱生活的程序员，喜欢旅行、摄影和美食，寻找有趣的灵魂一起探索世界",
                "profile_data": {
                    "age": 26,
                    "height": 175,
                    "education": "本科",
                    "occupation": "软件工程师",
                    "hobbies": ["摄影", "旅行", "美食", "电影", "健身", "读书"],
                    "personality": ["幽默", "细心", "上进", "温柔"]
                },
                "tags": ["程序员", "摄影爱好者", "旅行达人", "美食家", "健身", "不吸烟"]
            },
            {
                "id": "profile_activity_organizer_001",
                "scene_type": "activity",
                "role_type": "activity_organizer",
                "display_name": "活动达人小李",
                "bio": "热衷于组织各种有趣的活动，让大家在忙碌的生活中找到乐趣和朋友",
                "profile_data": {
                    "organizing_experience": "2年",
                    "specialties": ["户外徒步", "摄影聚会", "美食探店", "技术分享", "桌游聚会"],
                    "group_size_preference": "10-20人",
                    "frequency": "每周1-2次"
                },
                "tags": ["活动组织者", "户外达人", "摄影爱好者", "美食探索", "技术分享", "社交达人"]
            },
            {
                "id": "profile_activity_participant_001",
                "scene_type": "activity",
                "role_type": "activity_participant",
                "display_name": "爱玩小李",
                "bio": "喜欢参加各种有趣的活动，结交新朋友，体验不同的生活方式",
                "profile_data": {
                    "interests": ["摄影", "徒步", "美食", "电影", "音乐", "旅行", "技术"],
                    "availability": {
                        "weekdays": "晚上7点后",
                        "weekends": "全天",
                        "holidays": "全天"
                    }
                },
                "tags": ["活动爱好者", "摄影新手", "户外运动", "美食爱好", "社交活跃", "周末有空"]
            }
        ]
    }
    
    print(f"👤 用户ID: {user_profiles['user_id']}")
    print(f"📊 总资料数: {user_profiles['total_count']}")
    print(f"✅ 激活资料数: {user_profiles['active_count']}")
    print()
    
    # 按场景分组展示
    scenes = {}
    for profile in user_profiles['profiles']:
        scene = profile['scene_type']
        if scene not in scenes:
            scenes[scene] = []
        scenes[scene].append(profile)
    
    scene_names = {
        'housing': '🏠 找房场景',
        'dating': '💕 交友场景',
        'activity': '🎯 活动场景'
    }
    
    for scene_type, profiles in scenes.items():
        print(f"{scene_names.get(scene_type, scene_type)}")
        print("-" * 40)
        
        for profile in profiles:
            print(f"  🎭 角色: {profile['role_type']}")
            print(f"  📝 显示名称: {profile['display_name']}")
            print(f"  💬 简介: {profile['bio']}")
            print(f"  🏷️  标签: {', '.join(profile['tags'])}")
            
            # 显示角色特定信息
            profile_data = profile['profile_data']
            
            if profile['role_type'] == 'housing_seeker':
                print(f"  💰 预算范围: {profile_data['budget_range'][0]}-{profile_data['budget_range'][1]}元")
                print(f"  📍 偏好区域: {', '.join(profile_data['preferred_areas'])}")
                print(f"  🏢 工作地点: {profile_data['company_location']}")
                
            elif profile['role_type'] == 'housing_provider':
                prop = profile_data['properties'][0]
                print(f"  🏠 房源地址: {prop['address']}")
                print(f"  💰 租金: {prop['rent']}元/月")
                print(f"  📐 面积: {prop['area']}平米")
                print(f"  🛠️  设施: {', '.join(prop['facilities'])}")
                
            elif profile['role_type'] == 'dating_seeker':
                print(f"  🎂 年龄: {profile_data['age']}岁")
                print(f"  📏 身高: {profile_data['height']}cm")
                print(f"  🎓 学历: {profile_data['education']}")
                print(f"  ❤️  兴趣: {', '.join(profile_data['hobbies'])}")
                print(f"  😊 性格: {', '.join(profile_data['personality'])}")
                
            elif profile['role_type'] == 'activity_organizer':
                print(f"  ⏰ 组织经验: {profile_data['organizing_experience']}")
                print(f"  🎯 专长领域: {', '.join(profile_data['specialties'])}")
                print(f"  👥 偏好人数: {profile_data['group_size_preference']}")
                print(f"  📅 活动频率: {profile_data['frequency']}")
                
            elif profile['role_type'] == 'activity_participant':
                print(f"  🎨 兴趣领域: {', '.join(profile_data['interests'])}")
                availability = profile_data['availability']
                print(f"  ⏰ 可参与时间:")
                for time_type, time_desc in availability.items():
                    print(f"    - {time_type}: {time_desc}")
            
            print()
        
        print()
    
    # API使用示例
    print("🔗 API使用示例")
    print("-" * 40)
    print("1. 获取所有角色资料:")
    print("   GET /users/me/profiles")
    print()
    print("2. 获取找房场景资料:")
    print("   GET /users/me/profiles/housing")
    print()
    print("3. 获取特定角色资料:")
    print("   GET /users/me/profiles/housing/housing_seeker")
    print()
    print("4. 创建新的角色资料:")
    print("   POST /users/me/profiles")
    print("   Content-Type: application/json")
    print("   Body: { role_type, scene_type, display_name, ... }")
    print()
    print("5. 更新角色资料:")
    print("   PUT /users/me/profiles/{profile_id}")
    print()
    print("6. 删除角色资料:")
    print("   DELETE /users/me/profiles/{profile_id}")
    print()
    
    print("✨ 用户角色资料系统演示完成！")
    print("=" * 60)

if __name__ == "__main__":
    demo_user_profiles()