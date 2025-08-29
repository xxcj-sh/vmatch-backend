#!/usr/bin/env python3
"""
创建用户角色资料表的数据库迁移脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.utils.db_config import DATABASE_URL

def create_user_profiles_table():
    """创建用户角色资料表"""
    engine = create_engine(DATABASE_URL)
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS user_profiles (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        role_type TEXT NOT NULL,
        scene_type TEXT NOT NULL,
        display_name TEXT NOT NULL,
        avatar_url TEXT,
        bio TEXT,
        profile_data TEXT,
        preferences TEXT,
        tags TEXT,
        is_active INTEGER DEFAULT 1,
        visibility TEXT DEFAULT 'public',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """
    
    create_indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_user_profiles_role_type ON user_profiles(role_type);",
        "CREATE INDEX IF NOT EXISTS idx_user_profiles_scene_type ON user_profiles(scene_type);"
    ]
    
    with engine.connect() as conn:
        # 创建表
        conn.execute(text(create_table_sql))
        
        # 创建索引
        for index_sql in create_indexes_sql:
            conn.execute(text(index_sql))
        
        conn.commit()
        print("用户角色资料表和索引创建成功！")

if __name__ == "__main__":
    create_user_profiles_table()