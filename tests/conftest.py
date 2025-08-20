import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)

@pytest.fixture
def auth_headers():
    """创建认证头"""
    # 测试模式下，使用测试用户ID作为token
    return {"Authorization": "Bearer user_001"}