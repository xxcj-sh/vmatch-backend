#!/usr/bin/env python3
"""
修复用户角色资料数据问题
"""

import sys
import os
import json
sys.path.append('.')

from sqlalchemy import create_engine, text
from app.utils.db_config import DATABASE_URL

def fix_user_profiles():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # 1. 检查 test_user_001 是否存在
        result = conn.execute(text("SELECT id FROM users WHERE id = 'test_user_001'"))
        user = result.fetchone()
        
        if not user:
            print("❌ test_user_001 用户不存在，正在创建...")
            # 创建用户
            conn.execute(text("""
                INSERT INTO users (id, username, email, hashed_password, is_active, nick_name)
                VALUES ('test_user_001', 'test_user_001', 'test_user_001@example.com', 'hashed_password', 1, 'Test User 001')
            """))
            conn.commit()
            print("✅ test_user_001 用户创建成功")
        else:
            print("✅ test_user_001 用户已存在")
        
        # 2. 清理现有的角色资料数据（如果有的话）
        conn.execute(text("DELETE FROM user_profiles WHERE user_id = 'test_user_001'"))
        conn.commit()
        print("🧹 清理了现有的角色资料数据")
        
        # 3. 插入新的角色资料数据
        profiles_data = [
            {
                "id": "profile_housing_seeker_001",
                "user_id": "test_user_001",
                "role_type": "housing_seeker",
                "scene_type": "housing",
                "display_name": "小李找房",
                "avatar_url": "https://example.com/avatars/housing_seeker.jpg",
                "bio": "刚毕业的程序员，寻找合适的合租房源，希望找到志同道合的室友",
                "profile_data": json.dumps({
                    "budget_range": [2000, 3500],
                    "preferred_areas": ["朝阳区", "海淀区", "昌平区"],
                    "room_type": "single_room",
                    "move_in_date": "2025-03-01",
                    "lease_duration": "12_months",
                    "lifestyle": "quiet",
                    "work_schedule": "9to6",
                    "pets": False,
                    "smoking": False,
                    "occupation": "软件工程师",
                    "company_location": "中关村"
                }),
                "preferences": json.dumps({
                    "roommate_gender": "any",
                    "roommate_age_range": [22, 35],
                    "shared_facilities": ["kitchen", "living_room"],
                    "transportation": ["subway", "bus"],
                    "nearby_facilities": ["supermarket", "gym", "restaurant"]
                }),
                "tags": json.dumps(["程序员", "安静", "整洁", "不吸烟", "无宠物", "朝九晚六"])
            },
            {
                "id": "profile_housing_provider_001",
                "user_id": "test_user_001",
                "role_type": "housing_provider",
                "scene_type": "housing",
                "display_name": "李房东",
                "avatar_url": "https://example.com/avatars/housing_provider.jpg",
                "bio": "有多套优质房源出租，环境优美，交通便利，欢迎咨询",
                "profile_data": json.dumps({
                    "properties": [
                        {
                            "id": "house_001",
                            "address": "北京市朝阳区望京SOHO",
                            "rent": 3200,
                            "room_type": "2室1厅",
                            "area": 85,
                            "floor": "15/30",
                            "available_date": "2025-02-15",
                            "facilities": ["空调", "洗衣机", "冰箱", "WiFi", "电梯"],
                            "images": ["house1_1.jpg", "house1_2.jpg", "house1_3.jpg"]
                        }
                    ],
                    "landlord_type": "individual",
                    "response_time": "within_2_hours",
                    "viewing_available": True,
                    "lease_terms": ["押一付三", "包物业费", "可短租"]
                }),
                "preferences": json.dumps({
                    "tenant_requirements": {
                        "stable_income": True,
                        "no_pets": False,
                        "no_smoking": True,
                        "quiet_lifestyle": True
                    },
                    "payment_methods": ["bank_transfer", "alipay", "wechat_pay"]
                }),
                "tags": json.dumps(["个人房东", "房源优质", "交通便利", "响应及时", "可看房"])
            },
            {
                "id": "profile_dating_seeker_001",
                "user_id": "test_user_001",
                "role_type": "dating_seeker",
                "scene_type": "dating",
                "display_name": "阳光小李",
                "avatar_url": "https://example.com/avatars/dating_seeker.jpg",
                "bio": "热爱生活的程序员，喜欢旅行、摄影和美食，寻找有趣的灵魂一起探索世界",
                "profile_data": json.dumps({
                    "age": 26,
                    "height": 175,
                    "education": "本科",
                    "occupation": "软件工程师",
                    "income_range": "10k-20k",
                    "relationship_status": "single",
                    "looking_for": "serious_relationship",
                    "hobbies": ["摄影", "旅行", "美食", "电影", "健身", "读书"],
                    "personality": ["幽默", "细心", "上进", "温柔"],
                    "lifestyle": {
                        "exercise_frequency": "3-4次/周",
                        "drinking": "社交饮酒",
                        "smoking": "不吸烟",
                        "diet": "无特殊要求"
                    }
                }),
                "preferences": json.dumps({
                    "age_range": [22, 30],
                    "height_range": [155, 170],
                    "education_level": ["本科", "硕士", "博士"],
                    "personality_preferences": ["温柔", "善良", "有趣", "独立"],
                    "lifestyle_preferences": {
                        "non_smoker": True,
                        "social_drinker_ok": True,
                        "active_lifestyle": True
                    },
                    "relationship_goals": "long_term"
                }),
                "tags": json.dumps(["程序员", "摄影爱好者", "旅行达人", "美食家", "健身", "不吸烟"])
            },
            {
                "id": "profile_activity_organizer_001",
                "user_id": "test_user_001",
                "role_type": "activity_organizer",
                "scene_type": "activity",
                "display_name": "活动达人小李",
                "avatar_url": "https://example.com/avatars/activity_organizer.jpg",
                "bio": "热衷于组织各种有趣的活动，让大家在忙碌的生活中找到乐趣和朋友",
                "profile_data": json.dumps({
                    "organizing_experience": "2年",
                    "specialties": ["户外徒步", "摄影聚会", "美食探店", "技术分享", "桌游聚会"],
                    "group_size_preference": "10-20人",
                    "frequency": "每周1-2次",
                    "locations": ["北京市内", "周边郊区"],
                    "past_activities": [
                        {
                            "name": "香山红叶摄影团",
                            "date": "2024-10-15",
                            "participants": 15,
                            "rating": 4.8
                        },
                        {
                            "name": "三里屯美食探店",
                            "date": "2024-11-20",
                            "participants": 12,
                            "rating": 4.6
                        }
                    ],
                    "contact_info": {
                        "wechat_group": True,
                        "qq_group": True,
                        "response_time": "1小时内"
                    }
                }),
                "preferences": json.dumps({
                    "participant_requirements": {
                        "age_range": [20, 40],
                        "active_participation": True,
                        "punctuality": True,
                        "positive_attitude": True
                    },
                    "activity_types": ["outdoor", "cultural", "food", "tech", "social"],
                    "weather_dependency": "flexible"
                }),
                "tags": json.dumps(["活动组织者", "户外达人", "摄影爱好者", "美食探索", "技术分享", "社交达人"])
            },
            {
                "id": "profile_activity_participant_001",
                "user_id": "test_user_001",
                "role_type": "activity_participant",
                "scene_type": "activity",
                "display_name": "爱玩小李",
                "avatar_url": "https://example.com/avatars/activity_participant.jpg",
                "bio": "喜欢参加各种有趣的活动，结交新朋友，体验不同的生活方式",
                "profile_data": json.dumps({
                    "interests": ["摄影", "徒步", "美食", "电影", "音乐", "旅行", "技术"],
                    "availability": {
                        "weekdays": "晚上7点后",
                        "weekends": "全天",
                        "holidays": "全天"
                    },
                    "experience_level": {
                        "outdoor_activities": "中级",
                        "photography": "初级",
                        "cooking": "初级",
                        "sports": "中级"
                    },
                    "transportation": ["地铁", "公交", "自驾"],
                    "budget_range": {
                        "low": 50,
                        "medium": 200,
                        "high": 500
                    }
                }),
                "preferences": json.dumps({
                    "activity_types": ["outdoor", "cultural", "food", "photography", "social"],
                    "group_size": "5-20人",
                    "duration": "2-6小时",
                    "difficulty_level": ["easy", "medium"],
                    "location_preference": "市内及周边"
                }),
                "tags": json.dumps(["活动爱好者", "摄影新手", "户外运动", "美食爱好", "社交活跃", "周末有空"])
            }
        ]
        
        # 插入数据
        for profile in profiles_data:
            insert_sql = """
            INSERT INTO user_profiles (
                id, user_id, role_type, scene_type, display_name, avatar_url, bio,
                profile_data, preferences, tags, is_active, visibility, created_at, updated_at
            ) VALUES (
                :id, :user_id, :role_type, :scene_type, :display_name, :avatar_url, :bio,
                :profile_data, :preferences, :tags, 1, 'public', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
            )
            """
            
            conn.execute(text(insert_sql), profile)
        
        conn.commit()
        print(f"✅ 成功插入了 {len(profiles_data)} 个角色资料！")
        
        # 验证插入结果
        result = conn.execute(text("SELECT COUNT(*) FROM user_profiles WHERE user_id = 'test_user_001'"))
        count = result.fetchone()[0]
        print(f"📊 验证：数据库中现有 {count} 个 test_user_001 的角色资料")
        
        # 显示资料列表
        result = conn.execute(text("SELECT role_type, scene_type, display_name FROM user_profiles WHERE user_id = 'test_user_001'"))
        profiles = result.fetchall()
        print("📋 资料列表:")
        for profile in profiles:
            print(f"  - {profile[1]}.{profile[0]}: {profile[2]}")

if __name__ == "__main__":
    fix_user_profiles()