import os
import sys
from sqlalchemy import text

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.db_config import engine, SessionLocal
from app.utils.db_init import init_db
from app.models import User, Match, MatchDetail

def test_connection():
    """测试数据库连接"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("数据库连接成功!")
            return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False

def create_test_data():
    """创建测试数据"""
    db = SessionLocal()
    try:
        # 检查是否已有用户
        user_count = db.query(User).count()
        if user_count > 0:
            print(f"数据库中已有 {user_count} 个用户，跳过测试数据创建")
            return
        
        # 创建测试用户
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password",  # 实际应用中应使用哈希密码
            is_active=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        # 创建测试匹配
        test_match = Match(
            user_id=test_user.id,
            match_type="dating",
            status="active",
            score=85.5
        )
        db.add(test_match)
        db.commit()
        db.refresh(test_match)
        
        # 创建测试匹配详情
        test_details = [
            MatchDetail(
                match_id=test_match.id,
                detail_type="interest",
                detail_value="编程"
            ),
            MatchDetail(
                match_id=test_match.id,
                detail_type="location",
                detail_value="北京"
            )
        ]
        db.add_all(test_details)
        db.commit()
        
        print("测试数据创建成功!")
    except Exception as e:
        db.rollback()
        print(f"创建测试数据失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("初始化数据库...")
    
    # 初始化数据库表
    init_db()
    
    # 测试数据库连接
    if test_connection():
        # 创建测试数据
        create_test_data()
    
    print("数据库初始化完成!")