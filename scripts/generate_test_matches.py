#!/usr/bin/env python3
"""
生成测试匹配数据脚本
为测试用户 test_user_001 创建活动类型的匹配数据
"""

import sys
import os
from datetime import datetime, timedelta
import random

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.database import get_db
from app.models.match import Match
from app.models.user import User
from sqlalchemy.orm import Session

def generate_test_matches():
    """为测试用户生成匹配数据"""
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 检查测试用户是否存在
        test_user = db.query(User).filter(User.username == "test_user_001").first()
        if not test_user:
            print("测试用户 test_user_001 不存在，请先创建用户")
            return
        
        print(f"找到测试用户: {test_user.username} (ID: {test_user.id})")
        
        # 清理现有的测试数据
        existing_matches = db.query(Match).filter(
            (Match.user1_id == test_user.id) | (Match.user2_id == test_user.id)
        ).all()
        
        for match in existing_matches:
            db.delete(match)
        
        print(f"清理了 {len(existing_matches)} 条现有匹配记录")
        
        # 生成测试匹配数据
        test_matches = []
        
        # 创建一些其他测试用户作为匹配对象
        other_users = []
        for i in range(2, 6):  # 创建 test_user_002 到 test_user_005
            username = f"test_user_{i:03d}"
            user = db.query(User).filter(User.username == username).first()
            if not user:
                user = User(
                    username=username,
                    email=f"{username}@test.com",
                    phone=f"1380000{i:04d}",
                    nickname=f"测试用户{i}",
                    gender="male" if i % 2 == 0 else "female",
                    age=20 + i,
                    location="北京市",
                    bio=f"这是测试用户{i}的简介",
                    avatar_url=f"https://example.com/avatar{i}.jpg",
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(user)
                db.flush()
            other_users.append(user)
        
        print(f"准备了 {len(other_users)} 个其他测试用户")
        
        # 生成不同状态的匹配记录
        match_statuses = ["pending", "accepted", "rejected", "expired"]
        match_types = ["activity"]  # 专门生成 activity 类型
        
        for i in range(15):  # 生成15条匹配记录
            other_user = random.choice(other_users)
            status = random.choice(match_statuses)
            match_type = "activity"
            
            # 随机决定谁是发起者
            if random.choice([True, False]):
                user1_id = test_user.id
                user2_id = other_user.id
            else:
                user1_id = other_user.id
                user2_id = test_user.id
            
            # 创建时间在过去30天内
            created_at = datetime.utcnow() - timedelta(days=random.randint(0, 30))
            updated_at = created_at + timedelta(hours=random.randint(0, 48))
            
            # 根据状态设置过期时间
            if status == "expired":
                expires_at = created_at + timedelta(hours=24)  # 已过期
            else:
                expires_at = created_at + timedelta(days=7)  # 7天后过期
            
            match = Match(
                user1_id=user1_id,
                user2_id=user2_id,
                match_type=match_type,
                status=status,
                activity_id=f"activity_{random.randint(1000, 9999)}",
                activity_name=f"测试活动{random.randint(1, 100)}",
                activity_location="北京市朝阳区",
                activity_time=created_at + timedelta(days=random.randint(1, 14)),
                message=f"这是第{i+1}条测试匹配消息" if random.choice([True, False]) else None,
                created_at=created_at,
                updated_at=updated_at,
                expires_at=expires_at
            )
            
            test_matches.append(match)
            db.add(match)
        
        # 提交所有更改
        db.commit()
        
        print(f"成功生成了 {len(test_matches)} 条测试匹配记录")
        
        # 显示生成的数据统计
        status_counts = {}
        for match in test_matches:
            status_counts[match.status] = status_counts.get(match.status, 0) + 1
        
        print("\n生成的匹配数据统计:")
        for status, count in status_counts.items():
            print(f"  {status}: {count} 条")
        
        print(f"\n测试用户 {test_user.username} 的匹配数据已生成完成")
        print("可以使用以下API进行测试:")
        print("GET /api/v1/matches?status=null&page=1&pageSize=10&matchType=activity")
        
    except Exception as e:
        db.rollback()
        print(f"生成测试数据时出错: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    generate_test_matches()