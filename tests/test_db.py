import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Match, MatchDetail
from app.utils.db_config import Base
from app.services import db_service

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # 创建测试数据库
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def tearDown(self):
        # 清理测试数据库
        Base.metadata.drop_all(self.engine)
        
    def test_create_user(self):
        # 测试创建用户
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "hashedpassword"
        }
        user = db_service.create_user(self.session, user_data)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        
    def test_create_match(self):
        # 创建测试用户
        user_data = {
            "username": "matchuser",
            "email": "match@example.com",
            "hashed_password": "hashedpassword"
        }
        user = db_service.create_user(self.session, user_data)
        
        # 测试创建匹配
        match_data = {
            "user_id": user.id,
            "match_type": "test_type",
            "status": "pending",
            "score": 85.5
        }
        details = [
            {"detail_type": "preference", "detail_value": "sports"},
            {"detail_type": "location", "detail_value": "Beijing"}
        ]
        
        match = db_service.create_match(self.session, match_data, details)
        self.assertEqual(match.user_id, user.id)
        self.assertEqual(match.match_type, "test_type")
        
        # 测试获取匹配详情
        match_details = db_service.get_match_details(self.session, match.id)
        self.assertEqual(len(match_details), 2)
        self.assertEqual(match_details[0].detail_type, "preference")
        self.assertEqual(match_details[1].detail_value, "Beijing")
        
    def test_update_user(self):
        # 创建测试用户
        user_data = {
            "username": "updateuser",
            "email": "update@example.com",
            "hashed_password": "hashedpassword"
        }
        user = db_service.create_user(self.session, user_data)
        
        # 测试更新用户
        update_data = {
            "username": "updateduser",
            "is_active": False
        }
        updated_user = db_service.update_user(self.session, user.id, update_data)
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.is_active, False)
        self.assertEqual(updated_user.email, "update@example.com")  # 未更新的字段保持不变
        
    def test_delete_match(self):
        # 创建测试用户
        user_data = {
            "username": "deleteuser",
            "email": "delete@example.com",
            "hashed_password": "hashedpassword"
        }
        user = db_service.create_user(self.session, user_data)
        
        # 创建测试匹配
        match_data = {
            "user_id": user.id,
            "match_type": "delete_test",
            "status": "active",
            "score": 90.0
        }
        match = db_service.create_match(self.session, match_data)
        
        # 添加匹配详情
        detail_data = {
            "detail_type": "test",
            "detail_value": "value"
        }
        db_service.add_match_detail(self.session, match.id, detail_data)
        
        # 测试删除匹配
        success = db_service.delete_match(self.session, match.id)
        self.assertTrue(success)
        
        # 验证匹配已删除
        deleted_match = db_service.get_match(self.session, match.id)
        self.assertIsNone(deleted_match)
        
        # 验证匹配详情已删除
        match_details = db_service.get_match_details(self.session, match.id)
        self.assertEqual(len(match_details), 0)

if __name__ == "__main__":
    unittest.main()