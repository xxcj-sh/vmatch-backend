#!/usr/bin/env python3
"""
使用SQLAlchemy设置测试数据脚本
为测试用户 test_user_001 创建匹配测试数据
"""

import sys
import os
from datetime import datetime, timedelta

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.database import get_db, engine, Base
from app.models.user import User
from app.models.match import Match
from sqlalchemy.orm import Session

def setup_test_data():
    """设置测试数据"""
    
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("数据库表已创建/验证")
        
        # 获取数据库会话
        db = next(get_db())
        
        print("开始设置测试数据...")
        
        # 1. 创建测试用户
        test_users_data = [
            ('test_user_001', 'test_user_001@test.com', '13800000001', '测试用户001', 'male', 25, '北京市', '这是测试用户001'),
            ('test_user_002', 'test_user_002@test.com', '13800000002', '测试用户002', 'female', 23, '北京市', '这是测试用户002'),
            ('test_user_003', 'test_user_003@test.com', '13800000003', '测试用户003', 'male', 27, '北京市', '这是测试用户003'),
            ('test_user_004', 'test_user_004@test.com', '13800000004', '测试用户004', 'female', 24, '北京市', '这是测试用户004'),
            ('test_user_005', 'test_user_005@test.com', '13800000005', '测试用户005', 'male', 26, '北京市', '这是测试用户005'),
        ]
        
        users = {}
        for username, email, phone, nickname, gender, age, location, bio in test_users_data:
            # 检查用户是否已存在
            existing_user = db.query(User).filter(User.username == username).first()
            if existing_user:
                users[username] = existing_user
                print(f"用户 {username} 已存在")
            else:
                user = User(
                    username=username,
                    email=email,
                    phone=phone,
                    nickname=nickname,
                    gender=gender,
                    age=age,
                    location=location,
                    bio=bio,
                    avatar_url=f'https://example.com/avatar{username[-3:]}.jpg',
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(user)
                db.flush()  # 获取ID
                users[username] = user
                print(f"创建用户 {username}")
        
        print(f"准备了 {len(users)} 个测试用户")
        
        # 2. 清理现有匹配数据
        test_user_ids = [user.id for user in users.values()]
        existing_matches = db.query(Match).filter(
            (Match.user1_id.in_(test_user_ids)) | (Match.user2_id.in_(test_user_ids))
        ).all()
        
        for match in existing_matches:
            db.delete(match)
        
        print(f"清理了 {len(existing_matches)} 条现有匹配记录")
        
        # 3. 创建测试匹配数据
        now = datetime.utcnow()
        
        test_matches_data = [
            # (user1, user2, status, activity_name, location, message, activity_days_offset, created_days_offset, expires_days_offset)
            ('test_user_001', 'test_user_002', 'pending', '周末户外徒步', '北京市海淀区香山公园', '一起去香山徒步吧！', 3, -1, 6),
            ('test_user_003', 'test_user_001', 'pending', '咖啡厅读书会', '北京市朝阳区三里屯', '想找个人一起读书', 2, 0, 6),
            ('test_user_001', 'test_user_004', 'pending', '电影院看新片', '北京市西城区西单大悦城', None, 1, 0, 6),
            ('test_user_005', 'test_user_001', 'pending', '羽毛球运动', '北京市朝阳区体育馆', '找球友一起打球', 6, 0, 6),
            ('test_user_002', 'test_user_001', 'pending', '公园跑步', '北京市朝阳区奥林匹克森林公园', '晨跑爱好者', 3, 0, 6),
            
            ('test_user_001', 'test_user_005', 'accepted', '健身房运动', '北京市朝阳区健身中心', '一起健身！', 4, -3, 4),
            ('test_user_002', 'test_user_001', 'accepted', '美术馆参观', '北京市东城区中国美术馆', '对艺术很感兴趣', 5, -4, 3),
            ('test_user_001', 'test_user_003', 'accepted', '公园散步', '北京市海淀区圆明园', '天气不错，一起散步', 2, -1, 6),
            ('test_user_001', 'test_user_004', 'accepted', '餐厅聚餐', '北京市西城区王府井', '尝试新餐厅', 1, -2, 5),
            
            ('test_user_004', 'test_user_001', 'rejected', '音乐会欣赏', '北京市西城区国家大剧院', '古典音乐爱好者', 7, -5, 2),
            ('test_user_001', 'test_user_005', 'rejected', '博物馆参观', '北京市东城区故宫博物院', None, 3, -6, 1),
            ('test_user_001', 'test_user_003', 'rejected', 'KTV唱歌', '北京市海淀区中关村', None, 2, -7, 0),
            
            ('test_user_003', 'test_user_001', 'expired', '图书馆学习', '北京市海淀区国家图书馆', '一起学习提升', -1, -8, -1),
            ('test_user_001', 'test_user_002', 'expired', '购物中心逛街', '北京市朝阳区国贸商城', '周末逛街', -2, -10, -3),
            ('test_user_004', 'test_user_001', 'expired', '游泳健身', '北京市东城区游泳馆', '游泳爱好者', -3, -12, -5),
        ]
        
        matches = []
        for i, (user1_name, user2_name, status, activity_name, location, message, activity_offset, created_offset, expires_offset) in enumerate(test_matches_data):
            activity_time = now + timedelta(days=activity_offset)
            created_at = now + timedelta(days=created_offset)
            updated_at = created_at + timedelta(hours=1)  # 稍后更新
            expires_at = now + timedelta(days=expires_offset)
            
            match = Match(
                user1_id=users[user1_name].id,
                user2_id=users[user2_name].id,
                match_type='activity',
                status=status,
                activity_id=f'activity_{1001 + i}',
                activity_name=activity_name,
                activity_location=location,
                activity_time=activity_time,
                message=message,
                created_at=created_at,
                updated_at=updated_at,
                expires_at=expires_at
            )
            
            matches.append(match)
            db.add(match)
        
        print(f"创建了 {len(matches)} 条测试匹配记录")
        
        # 提交所有更改
        db.commit()
        
        # 4. 验证数据
        test_user_001 = users['test_user_001']
        verification_matches = db.query(Match).filter(
            ((Match.user1_id == test_user_001.id) | (Match.user2_id == test_user_001.id)) &
            (Match.match_type == 'activity')
        ).order_by(Match.created_at.desc()).all()
        
        print(f"\n✅ 验证结果: 找到 {len(verification_matches)} 条匹配记录")
        
        # 统计各状态数量
        status_counts = {}
        for match in verification_matches:
            status_counts[match.status] = status_counts.get(match.status, 0) + 1
        
        print(f"\n状态统计:")
        for status, count in status_counts.items():
            print(f"  {status}: {count} 条")
        
        print(f"\n匹配记录详情:")
        print("ID | 状态 | 活动名称 | 位置 | 创建时间")
        print("-" * 80)
        for match in verification_matches[:10]:  # 显示前10条
            print(f"{match.id} | {match.status} | {match.activity_name} | {match.activity_location} | {match.created_at}")
        
        if len(verification_matches) > 10:
            print(f"... 还有 {len(verification_matches) - 10} 条记录")
        
        print(f"\n✅ 测试数据设置完成！")
        print("现在可以使用以下API进行测试:")
        print("GET /api/v1/matches?status=null&page=1&pageSize=10&matchType=activity")
        print(f"测试用户ID: {test_user_001.id}")
        
    except Exception as e:
        print(f"❌ 设置测试数据时出错: {str(e)}")
        if 'db' in locals():
            db.rollback()
        raise
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    setup_test_data()