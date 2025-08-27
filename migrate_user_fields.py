#!/usr/bin/env python3
"""
数据库迁移脚本：为User表添加新字段
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.utils.db_config import Base, engine
from app.models.user import User

def migrate_user_table():
    """迁移用户表，添加新字段"""
    print("开始迁移用户表...")
    
    try:
        # 检查表是否存在
        with engine.connect() as conn:
            # 获取现有列信息
            result = conn.execute(text("PRAGMA table_info(users)"))
            existing_columns = {row[1] for row in result.fetchall()}
            print(f"现有列: {existing_columns}")
            
            # 需要添加的新列
            new_columns = {
                'nick_name': 'VARCHAR',
                'avatar_url': 'VARCHAR',
                'gender': 'INTEGER',
                'age': 'INTEGER',
                'occupation': 'VARCHAR',
                'location': 'JSON',
                'bio': 'TEXT',
                'match_type': 'VARCHAR',
                'user_role': 'VARCHAR',
                'interests': 'JSON',
                'preferences': 'JSON',
                'phone': 'VARCHAR',
                'education': 'VARCHAR',
                'join_date': 'INTEGER'
            }
            
            # 添加缺失的列
            for column_name, column_type in new_columns.items():
                if column_name not in existing_columns:
                    try:
                        sql = f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"
                        conn.execute(text(sql))
                        print(f"添加列: {column_name}")
                    except Exception as e:
                        print(f"添加列 {column_name} 时出错: {e}")
            
            conn.commit()
            print("用户表迁移完成！")
            
    except Exception as e:
        print(f"迁移过程中出错: {e}")
        return False
    
    return True

def verify_migration():
    """验证迁移结果"""
    print("\n验证迁移结果...")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result.fetchall()]
            print(f"迁移后的列: {columns}")
            
            # 检查是否包含所有必要的列
            required_columns = [
                'nick_name', 'avatar_url', 'gender', 'age', 'occupation',
                'location', 'bio', 'match_type', 'user_role', 'interests',
                'preferences', 'phone', 'education', 'join_date'
            ]
            
            missing_columns = [col for col in required_columns if col not in columns]
            if missing_columns:
                print(f"警告：缺失列: {missing_columns}")
                return False
            else:
                print("✓ 所有必要列都已添加")
                return True
                
    except Exception as e:
        print(f"验证过程中出错: {e}")
        return False

if __name__ == "__main__":
    print("用户表字段迁移脚本")
    print("=" * 50)
    
    # 执行迁移
    if migrate_user_table():
        # 验证迁移
        if verify_migration():
            print("\n✓ 迁移成功完成！")
        else:
            print("\n✗ 迁移验证失败")
            sys.exit(1)
    else:
        print("\n✗ 迁移失败")
        sys.exit(1)