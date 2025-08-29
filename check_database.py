#!/usr/bin/env python3
"""
检查数据库中的用户角色资料数据
"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine, text
from app.utils.db_config import DATABASE_URL

def check_database():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # 检查表是否存在
        try:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='user_profiles'"))
            table_exists = result.fetchone()
            
            if not table_exists:
                print("❌ user_profiles 表不存在")
                return
            else:
                print("✅ user_profiles 表存在")
        except Exception as e:
            print(f"❌ 检查表存在性时出错: {e}")
            return
        
        # 检查数据数量
        try:
            result = conn.execute(text("SELECT COUNT(*) as count FROM user_profiles WHERE user_id = 'test_user_001'"))
            count = result.fetchone()[0]
            print(f"📊 数据库中 test_user_001 的资料数量: {count}")
            
            if count > 0:
                result = conn.execute(text("SELECT id, role_type, scene_type, display_name FROM user_profiles WHERE user_id = 'test_user_001'"))
                profiles = result.fetchall()
                print("📋 资料列表:")
                for profile in profiles:
                    print(f"  - {profile[1]}.{profile[2]}: {profile[3]}")
            else:
                print("❌ 没有找到资料数据")
                
                # 检查是否有任何数据
                result = conn.execute(text("SELECT COUNT(*) as total FROM user_profiles"))
                total = result.fetchone()[0]
                print(f"📊 数据库中总资料数量: {total}")
                
        except Exception as e:
            print(f"❌ 查询数据时出错: {e}")

if __name__ == "__main__":
    check_database()