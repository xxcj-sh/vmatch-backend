#!/usr/bin/env python3
"""
测试匹配API的脚本
验证生成的测试数据是否能正确响应API查询
"""

import sys
import os
import requests
import json

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_matches_api():
    """测试匹配API"""
    
    # API基础URL (根据实际部署调整)
    base_url = "http://localhost:8000"  # 假设FastAPI运行在8000端口
    
    # 测试查询参数
    test_queries = [
        {
            "name": "查询所有activity类型匹配",
            "url": f"{base_url}/api/v1/matches?status=null&page=1&pageSize=10&matchType=activity",
            "headers": {"Authorization": "Bearer test_user_001_token"}  # 需要根据实际认证方式调整
        },
        {
            "name": "查询pending状态的activity匹配",
            "url": f"{base_url}/api/v1/matches?status=pending&page=1&pageSize=5&matchType=activity",
            "headers": {"Authorization": "Bearer test_user_001_token"}
        },
        {
            "name": "查询accepted状态的activity匹配",
            "url": f"{base_url}/api/v1/matches?status=accepted&page=1&pageSize=5&matchType=activity",
            "headers": {"Authorization": "Bearer test_user_001_token"}
        },
        {
            "name": "查询第二页数据",
            "url": f"{base_url}/api/v1/matches?status=null&page=2&pageSize=5&matchType=activity",
            "headers": {"Authorization": "Bearer test_user_001_token"}
        }
    ]
    
    print("开始测试匹配API...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"URL: {test_case['url']}")
        
        try:
            # 发送GET请求
            response = requests.get(test_case['url'], headers=test_case.get('headers', {}))
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 请求成功")
                
                # 显示响应数据摘要
                if isinstance(data, dict):
                    if 'data' in data and isinstance(data['data'], list):
                        print(f"返回记录数: {len(data['data'])}")
                        if data['data']:
                            print("前3条记录:")
                            for j, match in enumerate(data['data'][:3]):
                                print(f"  {j+1}. ID:{match.get('id')} 状态:{match.get('status')} 活动:{match.get('activity_name')}")
                    
                    if 'total' in data:
                        print(f"总记录数: {data['total']}")
                    if 'page' in data:
                        print(f"当前页: {data['page']}")
                    if 'pageSize' in data:
                        print(f"页大小: {data['pageSize']}")
                
            else:
                print(f"❌ 请求失败")
                print(f"响应内容: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 连接失败 - 请确保API服务器正在运行")
        except Exception as e:
            print(f"❌ 请求出错: {str(e)}")
        
        print("-" * 40)
    
    print(f"\n测试完成！")
    print("\n注意事项:")
    print("1. 请确保FastAPI服务器正在运行 (python -m app.main)")
    print("2. 根据实际的认证方式调整请求头")
    print("3. 根据实际的API端口调整base_url")

def test_direct_database_query():
    """直接查询数据库验证数据"""
    
    try:
        from app.models.database import get_db
        from app.models.match import Match
        from app.models.user import User
        
        db = next(get_db())
        
        print("\n直接数据库查询验证:")
        print("=" * 40)
        
        # 查询test_user_001的所有activity匹配
        test_user = db.query(User).filter(User.username == "test_user_001").first()
        if not test_user:
            print("❌ 测试用户不存在")
            return
        
        matches = db.query(Match).filter(
            ((Match.user1_id == test_user.id) | (Match.user2_id == test_user.id)) &
            (Match.match_type == 'activity')
        ).order_by(Match.created_at.desc()).all()
        
        print(f"✅ 找到 {len(matches)} 条匹配记录")
        
        # 按状态统计
        status_counts = {}
        for match in matches:
            status_counts[match.status] = status_counts.get(match.status, 0) + 1
        
        print("\n状态分布:")
        for status, count in status_counts.items():
            print(f"  {status}: {count} 条")
        
        print(f"\n前5条记录详情:")
        for i, match in enumerate(matches[:5]):
            other_user_id = match.user2_id if match.user1_id == test_user.id else match.user1_id
            other_user = db.query(User).filter(User.id == other_user_id).first()
            print(f"  {i+1}. [{match.status}] {match.activity_name} - 与 {other_user.nickname if other_user else 'Unknown'}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 数据库查询出错: {str(e)}")

if __name__ == "__main__":
    # 先进行直接数据库查询验证
    test_direct_database_query()
    
    # 然后测试API (需要服务器运行)
    print("\n" + "="*60)
    test_matches_api()