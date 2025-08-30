#!/usr/bin/env python3
"""
设置测试数据脚本
为测试用户 test_user_001 创建匹配测试数据
"""

import sys
import os
from datetime import datetime, timedelta
import sqlite3

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_test_data():
    """设置测试数据"""
    
    # 数据库文件路径 (根据实际项目配置调整)
    db_path = "vmatch.db"  # 或者从配置文件读取
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("开始设置测试数据...")
        
        # 1. 创建测试用户
        test_users = [
            ('test_user_001', 'test_user_001@test.com', '13800000001', '测试用户001', 'male', 25, '北京市', '这是测试用户001', 'https://example.com/avatar1.jpg'),
            ('test_user_002', 'test_user_002@test.com', '13800000002', '测试用户002', 'female', 23, '北京市', '这是测试用户002', 'https://example.com/avatar2.jpg'),
            ('test_user_003', 'test_user_003@test.com', '13800000003', '测试用户003', 'male', 27, '北京市', '这是测试用户003', 'https://example.com/avatar3.jpg'),
            ('test_user_004', 'test_user_004@test.com', '13800000004', '测试用户004', 'female', 24, '北京市', '这是测试用户004', 'https://example.com/avatar4.jpg'),
            ('test_user_005', 'test_user_005@test.com', '13800000005', '测试用户005', 'male', 26, '北京市', '这是测试用户005', 'https://example.com/avatar5.jpg'),
        ]
        
        for user_data in test_users:
            cursor.execute("""
                INSERT OR IGNORE INTO users (
                    username, email, phone, nickname, gender, age, location, bio, 
                    avatar_url, is_active, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, datetime('now'), datetime('now'))
            """, user_data)
        
        print(f"创建了 {len(test_users)} 个测试用户")
        
        # 2. 获取用户ID
        user_ids = {}
        for username, *_ in test_users:
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                user_ids[username] = result[0]
        
        print(f"获取了 {len(user_ids)} 个用户ID")
        
        # 3. 清理现有匹配数据
        test_user_ids = list(user_ids.values())
        placeholders = ','.join(['?' for _ in test_user_ids])
        cursor.execute(f"""
            DELETE FROM matches WHERE 
                user1_id IN ({placeholders}) OR user2_id IN ({placeholders})
        """, test_user_ids + test_user_ids)
        
        print("清理了现有的测试匹配数据")
        
        # 4. 创建测试匹配数据
        test_matches = [
            # pending 状态
            (user_ids['test_user_001'], user_ids['test_user_002'], 'activity', 'pending', 'activity_1001', '周末户外徒步', '北京市海淀区香山公园', '一起去香山徒步吧！', 3, -1, 6),
            (user_ids['test_user_003'], user_ids['test_user_001'], 'activity', 'pending', 'activity_1002', '咖啡厅读书会', '北京市朝阳区三里屯', '想找个人一起读书', 2, 0, 6),
            (user_ids['test_user_001'], user_ids['test_user_004'], 'activity', 'pending', 'activity_1003', '电影院看新片', '北京市西城区西单大悦城', None, 1, 0, 6),
            
            # accepted 状态
            (user_ids['test_user_001'], user_ids['test_user_005'], 'activity', 'accepted', 'activity_1004', '健身房运动', '北京市朝阳区健身中心', '一起健身！', 4, -3, 4),
            (user_ids['test_user_002'], user_ids['test_user_001'], 'activity', 'accepted', 'activity_1005', '美术馆参观', '北京市东城区中国美术馆', '对艺术很感兴趣', 5, -4, 3),
            (user_ids['test_user_001'], user_ids['test_user_003'], 'activity', 'accepted', 'activity_1006', '公园散步', '北京市海淀区圆明园', '天气不错，一起散步', 2, -1, 6),
            
            # rejected 状态
            (user_ids['test_user_004'], user_ids['test_user_001'], 'activity', 'rejected', 'activity_1007', '音乐会欣赏', '北京市西城区国家大剧院', '古典音乐爱好者', 7, -5, 2),
            (user_ids['test_user_001'], user_ids['test_user_005'], 'activity', 'rejected', 'activity_1008', '博物馆参观', '北京市东城区故宫博物院', None, 3, -6, 1),
            
            # expired 状态
            (user_ids['test_user_003'], user_ids['test_user_001'], 'activity', 'expired', 'activity_1009', '图书馆学习', '北京市海淀区国家图书馆', '一起学习提升', -1, -8, -1),
            (user_ids['test_user_001'], user_ids['test_user_002'], 'activity', 'expired', 'activity_1010', '购物中心逛街', '北京市朝阳区国贸商城', '周末逛街', -2, -10, -3),
            
            # 更多测试数据
            (user_ids['test_user_005'], user_ids['test_user_001'], 'activity', 'pending', 'activity_1011', '羽毛球运动', '北京市朝阳区体育馆', '找球友一起打球', 6, 0, 6),
            (user_ids['test_user_001'], user_ids['test_user_004'], 'activity', 'accepted', 'activity_1012', '餐厅聚餐', '北京市西城区王府井', '尝试新餐厅', 1, -2, 5),
            (user_ids['test_user_002'], user_ids['test_user_001'], 'activity', 'pending', 'activity_1013', '公园跑步', '北京市朝阳区奥林匹克森林公园', '晨跑爱好者', 3, 0, 6),
            (user_ids['test_user_001'], user_ids['test_user_003'], 'activity', 'rejected', 'activity_1014', 'KTV唱歌', '北京市海淀区中关村', None, 2, -7, 0),
            (user_ids['test_user_004'], user_ids['test_user_001'], 'activity', 'expired', 'activity_1015', '游泳健身', '北京市东城区游泳馆', '游泳爱好者', -3, -12, -5),
        ]
        
        for match_data in test_matches:
            user1_id, user2_id, match_type, status, activity_id, activity_name, activity_location, message, activity_days, created_days, expires_days = match_data
            
            # 计算时间
            now = datetime.now()
            activity_time = now + timedelta(days=activity_days)
            created_at = now + timedelta(days=created_days)
            updated_at = created_at
            expires_at = now + timedelta(days=expires_days)
            
            cursor.execute("""
                INSERT INTO matches (
                    user1_id, user2_id, match_type, status, activity_id, activity_name, 
                    activity_location, activity_time, message, created_at, updated_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user1_id, user2_id, match_type, status, activity_id, activity_name,
                activity_location, activity_time.isoformat(), message, 
                created_at.isoformat(), updated_at.isoformat(), expires_at.isoformat()
            ))
        
        print(f"创建了 {len(test_matches)} 条测试匹配记录")
        
        # 提交更改
        conn.commit()
        
        # 5. 验证数据
        cursor.execute("""
            SELECT 
                m.id,
                u1.username as user1,
                u2.username as user2,
                m.match_type,
                m.status,
                m.activity_name,
                m.created_at
            FROM matches m
            JOIN users u1 ON m.user1_id = u1.id
            JOIN users u2 ON m.user2_id = u2.id
            WHERE (u1.username = 'test_user_001' OR u2.username = 'test_user_001')
                AND m.match_type = 'activity'
            ORDER BY m.created_at DESC
        """)
        
        results = cursor.fetchall()
        
        print(f"\n验证结果: 找到 {len(results)} 条匹配记录")
        print("\n匹配记录详情:")
        print("ID | 用户1 | 用户2 | 类型 | 状态 | 活动名称 | 创建时间")
        print("-" * 80)
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]}")
        
        # 统计各状态数量
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM matches m
            JOIN users u1 ON m.user1_id = u1.id
            JOIN users u2 ON m.user2_id = u2.id
            WHERE (u1.username = 'test_user_001' OR u2.username = 'test_user_001')
                AND m.match_type = 'activity'
            GROUP BY status
        """)
        
        status_counts = cursor.fetchall()
        print(f"\n状态统计:")
        for status, count in status_counts:
            print(f"  {status}: {count} 条")
        
        print(f"\n✅ 测试数据设置完成！")
        print("现在可以使用以下API进行测试:")
        print("GET /api/v1/matches?status=null&page=1&pageSize=10&matchType=activity")
        
    except Exception as e:
        print(f"❌ 设置测试数据时出错: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    setup_test_data()