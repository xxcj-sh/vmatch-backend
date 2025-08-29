#!/usr/bin/env python3
"""
创建测试用户资料数据
"""
import sys
sys.path.append('.')

from app.utils.db_config import get_db
from app.models.user_profile import UserProfile
from app.models.user import User
from sqlalchemy.orm import Session
import uuid

def create_test_data():
    """创建测试数据"""
    db = next(get_db())
    
    try:
        # 检查用户是否存在，如果不存在则创建
        user_id = "profile_housing_seeker_001"
        existing_user = db.query(User).filter(User.id == user_id).first()
        
        if not existing_user:
            # 创建用户，包含完整的基础信息
            new_user = User(
                id=user_id,
                username="housing_seeker_001",
                email="housing_seeker_001@example.com",
                hashed_password="test_password",
                is_active=True,
                nick_name="小张",
                age=28,
                gender=1,  # 1: 男性, 2: 女性
                occupation="软件工程师",
                location=["北京市", "朝阳区"],
                phone="13800138000",
                education="本科",
                interests=["编程", "阅读", "旅行", "音乐"],
                bio="热爱生活的程序员，寻找合适的租房"
            )
            db.add(new_user)
            print(f"创建用户: {user_id}")
        else:
            # 如果用户已存在，更新基础信息
            if not existing_user.age:  # 检查是否需要更新基础信息
                existing_user.nick_name = "小张"
                existing_user.age = 28
                existing_user.gender = 1
                existing_user.occupation = "软件工程师"
                existing_user.location = ["北京市", "朝阳区"]
                existing_user.phone = "13800138000"
                existing_user.education = "本科"
                existing_user.interests = ["编程", "阅读", "旅行", "音乐"]
                existing_user.bio = "热爱生活的程序员，寻找合适的租房"
                print(f"更新用户基础信息: {user_id}")
        
        # 检查是否已存在相应的资料
        existing_profile = db.query(UserProfile).filter(
            UserProfile.user_id == user_id,
            UserProfile.scene_type == "housing",
            UserProfile.role_type == "housing_seeker"
        ).first()
        
        if not existing_profile:
            # 创建用户资料
            profile_id = f"profile_housing_housing_seeker_{uuid.uuid4().hex[:8]}"
            new_profile = UserProfile(
                id=profile_id,
                user_id=user_id,
                role_type="housing_seeker",
                scene_type="housing",
                display_name="租房寻找者",
                avatar_url="https://example.com/avatar.jpg",
                bio="寻找合适的租房",
                profile_data={
                    "budget": "3000-5000",
                    "location_preference": ["朝阳区", "海淀区"],
                    "room_type": "一居室"
                },
                preferences={
                    "pet_friendly": True,
                    "furnished": True
                },
                tags=["年轻人", "上班族"],
                visibility="public",
                is_active=1
            )
            db.add(new_profile)
            print(f"创建用户资料: {profile_id}")
        
        db.commit()
        print("测试数据创建成功！")
        
        # 验证数据
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == user_id,
            UserProfile.scene_type == "housing",
            UserProfile.role_type == "housing_seeker"
        ).first()
        
        if profile:
            print(f"验证成功 - 资料ID: {profile.id}")
        else:
            print("验证失败 - 未找到创建的资料")
            
    except Exception as e:
        print(f"创建测试数据时出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()