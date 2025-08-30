#!/usr/bin/env python3
"""
简单的API测试
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_matches_endpoint():
    """测试匹配端点"""
    
    print("测试匹配API端点...")
    
    # 测试基本的匹配查询
    response = client.get("/api/v1/matches?status=null&page=1&pageSize=10&matchType=housing")
    
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'matches' in data['data']:
            print("✅ API响应结构正确，包含matches字段")
            matches = data['data']['matches']
            print(f"返回匹配记录数: {len(matches)}")
            
            if matches:
                print("第一条记录示例:")
                print(f"  ID: {matches[0].get('id')}")
                print(f"  状态: {matches[0].get('status')}")
                print(f"  类型: {matches[0].get('match_type')}")
        else:
            print("❌ API响应结构不正确")
    else:
        print("❌ API请求失败")

if __name__ == "__main__":
    test_matches_endpoint()