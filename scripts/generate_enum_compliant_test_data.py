#!/usr/bin/env python3
"""
生成符合枚举值要求的测试数据
为测试用户 test_user_001 创建完整的匹配数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from app.models.database import engine
from app.models.user import User
from app.models.match import Match, MatchDetail
from app.models.enums import *
import random
from datetime import datetime, timedelta
import json

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_user():
    """创建测试用户"""
    session = SessionLocal()
    try:
        # 检查用户是否已存在
        existing_user = session.query(User).filter(User.id == "test_user_001").first()
        if existing_user:
            print("测试用户 test_user_001 已存在")
            return existing_user
        
        # 创建新用户
        user = User(
            id="test_user_001",
            username="test_user_001",
            email="test_user_001@example.com",
            phone="13800138001",
            nickname="测试用户001",
            avatar_url="https://example.com/avatar/test_user_001.jpg",
            gender=Gender.MALE.value,
            age=28,
            location=Region.BEIJING.value,
            bio="这是一个测试用户账号，用于API接口测试",
            is_active=True
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        print(f"✅ 创建测试用户: {user.id}")
        return user
        
    except Exception as e:
        session.rollback()
        print(f"❌ 创建用户失败: {e}")
        return None
    finally:
        session.close()

def generate_activity_matches(session, user_id: str, count: int = 20):
    """生成活动匹配数据"""
    matches = []
    
    for i in range(count):
        match_id = f"activity_match_{i+1:03d}"
        
        # 随机选择枚举值
        status = random.choice(list(MatchStatus)).value
        activity_type = random.choice(list(ActivityType)).value
        skill_level = random.choice(list(SkillLevel)).value
        group_size = random.choice(list(GroupSize)).value
        budget = random.choice(list(ActivityBudget)).value
        region = random.choice(list(Region)).value
        duration = random.choice(list(Duration)).value
        intensity = random.choice(list(Intensity)).value
        
        # 创建匹配记录
        match = Match(
            id=match_id,
            user_id=user_id,
            match_type=MatchType.ACTIVITY.value,
            status=status,
            score=random.uniform(0.6, 0.95),
            is_active=True,
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        
        session.add(match)
        matches.append(match)
        
        # 创建详细信息
        details = [
            MatchDetail(match_id=match_id, detail_type="activity_name", detail_value=f"{activity_type}活动{i+1}"),
            MatchDetail(match_id=match_id, detail_type="activity_type", detail_value=activity_type),
            MatchDetail(match_id=match_id, detail_type="skill_level", detail_value=skill_level),
            MatchDetail(match_id=match_id, detail_type="group_size", detail_value=group_size),
            MatchDetail(match_id=match_id, detail_type="budget", detail_value=budget),
            MatchDetail(match_id=match_id, detail_type="location", detail_value=f"{region}测试地点{i+1}"),
            MatchDetail(match_id=match_id, detail_type="duration", detail_value=duration),
            MatchDetail(match_id=match_id, detail_type="intensity", detail_value=intensity),
            MatchDetail(match_id=match_id, detail_type="activity_time", detail_value=f"2024-12-{(i % 28) + 1:02d}T{10 + (i % 12)}:00:00Z"),
        ]
        
        for detail in details:
            session.add(detail)
    
    return matches

def generate_housing_matches(session, user_id: str, count: int = 20):
    """生成房源匹配数据"""
    matches = []
    
    for i in range(count):
        match_id = f"housing_match_{i+1:03d}"
        
        # 随机选择枚举值
        status = random.choice(list(MatchStatus)).value
        house_type = random.choice(list(HouseType)).value
        budget_range = random.choice(list(BudgetRange)).value
        decoration = random.choice(list(DecorationLevel)).value
        region = random.choice(list(Region)).value
        orientation = random.choice(list(Orientation)).value
        floor_level = random.choice(list(FloorLevel)).value
        
        # 随机选择设施
        all_facilities = list(Facility)
        selected_facilities = random.sample(all_facilities, random.randint(3, 8))
        facilities = [f.value for f in selected_facilities]
        
        # 创建匹配记录
        match = Match(
            id=match_id,
            user_id=user_id,
            match_type=MatchType.HOUSING.value,
            status=status,
            score=random.uniform(0.6, 0.95),
            is_active=True,
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        
        session.add(match)
        matches.append(match)
        
        # 创建详细信息
        details = [
            MatchDetail(match_id=match_id, detail_type="property_title", detail_value=f"{house_type} - {region}优质房源{i+1}"),
            MatchDetail(match_id=match_id, detail_type="house_type", detail_value=house_type),
            MatchDetail(match_id=match_id, detail_type="budget_range", detail_value=budget_range),
            MatchDetail(match_id=match_id, detail_type="decoration", detail_value=decoration),
            MatchDetail(match_id=match_id, detail_type="location", detail_value=f"{region}测试小区{i+1}"),
            MatchDetail(match_id=match_id, detail_type="orientation", detail_value=orientation),
            MatchDetail(match_id=match_id, detail_type="floor_level", detail_value=floor_level),
            MatchDetail(match_id=match_id, detail_type="facilities", detail_value=json.dumps(facilities, ensure_ascii=False)),
            MatchDetail(match_id=match_id, detail_type="rent_price", detail_value=str(random.randint(2000, 8000))),
        ]
        
        for detail in details:
            session.add(detail)
    
    return matches

def generate_dating_matches(session, user_id: str, count: int = 20):
    """生成交友匹配数据"""
    matches = []
    
    for i in range(count):
        match_id = f"dating_match_{i+1:03d}"
        
        # 随机选择枚举值
        status = random.choice(list(MatchStatus)).value
        education = random.choice(list(Education)).value
        income_range = random.choice(list(IncomeRange)).value
        height_range = random.choice(list(HeightRange)).value
        marital_status = random.choice(list(MaritalStatus)).value
        work_industry = random.choice(list(WorkIndustry)).value
        
        # 随机选择兴趣爱好
        all_interests = list(Interest)
        selected_interests = random.sample(all_interests, random.randint(3, 8))
        interests = [i.value for i in selected_interests]
        
        # 随机选择性格特质
        all_personalities = list(Personality)
        selected_personalities = random.sample(all_personalities, random.randint(2, 5))
        personalities = [p.value for p in selected_personalities]
        
        # 创建匹配记录
        match = Match(
            id=match_id,
            user_id=user_id,
            match_type=MatchType.DATING.value,
            status=status,
            score=random.uniform(0.6, 0.95),
            is_active=True,
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        
        session.add(match)
        matches.append(match)
        
        # 创建详细信息
        details = [
            MatchDetail(match_id=match_id, detail_type="education", detail_value=education),
            MatchDetail(match_id=match_id, detail_type="income_range", detail_value=income_range),
            MatchDetail(match_id=match_id, detail_type="height_range", detail_value=height_range),
            MatchDetail(match_id=match_id, detail_type="marital_status", detail_value=marital_status),
            MatchDetail(match_id=match_id, detail_type="work_industry", detail_value=work_industry),
            MatchDetail(match_id=match_id, detail_type="interests", detail_value=json.dumps(interests, ensure_ascii=False)),
            MatchDetail(match_id=match_id, detail_type="personalities", detail_value=json.dumps(personalities, ensure_ascii=False)),
            MatchDetail(match_id=match_id, detail_type="age", detail_value=str(random.randint(22, 35))),
        ]
        
        for detail in details:
            session.add(detail)
    
    return matches

def main():
    """主函数"""
    print("开始生成符合枚举值要求的测试数据...")
    print("=" * 60)
    
    # 创建测试用户
    user = create_test_user()
    if not user:
        print("❌ 无法创建测试用户，退出")
        return
    
    session = SessionLocal()
    try:
        # 清理现有的测试数据
        print("清理现有测试数据...")
        session.query(MatchDetail).filter(
            MatchDetail.match_id.like("activity_match_%") |
            MatchDetail.match_id.like("housing_match_%") |
            MatchDetail.match_id.like("dating_match_%")
        ).delete(synchronize_session=False)
        
        session.query(Match).filter(
            Match.id.like("activity_match_%") |
            Match.id.like("housing_match_%") |
            Match.id.like("dating_match_%")
        ).delete(synchronize_session=False)
        
        session.commit()
        
        # 生成新的测试数据
        print("生成活动匹配数据...")
        activity_matches = generate_activity_matches(session, user.id, 20)
        print(f"✅ 生成了 {len(activity_matches)} 条活动匹配记录")
        
        print("生成房源匹配数据...")
        housing_matches = generate_housing_matches(session, user.id, 20)
        print(f"✅ 生成了 {len(housing_matches)} 条房源匹配记录")
        
        print("生成交友匹配数据...")
        dating_matches = generate_dating_matches(session, user.id, 20)
        print(f"✅ 生成了 {len(dating_matches)} 条交友匹配记录")
        
        # 提交所有更改
        session.commit()
        
        print("\n数据生成完成！")
        print(f"总计生成: {len(activity_matches) + len(housing_matches) + len(dating_matches)} 条匹配记录")
        
        # 验证数据
        print("\n验证生成的数据...")
        total_matches = session.query(Match).filter(Match.user_id == user.id).count()
        total_details = session.query(MatchDetail).join(Match).filter(Match.user_id == user.id).count()
        
        print(f"数据库中的匹配记录数: {total_matches}")
        print(f"数据库中的详细信息数: {total_details}")
        
        # 按类型统计
        for match_type in [MatchType.ACTIVITY, MatchType.HOUSING, MatchType.DATING]:
            count = session.query(Match).filter(
                Match.user_id == user.id,
                Match.match_type == match_type.value
            ).count()
            print(f"{match_type.value} 类型匹配数: {count}")
        
        print("\n✅ 测试数据生成完成！现在可以测试API接口了。")
        
    except Exception as e:
        session.rollback()
        print(f"❌ 生成数据失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    main()