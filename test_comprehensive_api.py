#!/usr/bin/env python3
"""
全面的API测试
"""

from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_matches_with_different_params():
    """测试不同参数的匹配查询"""
    
    test_cases = [
        {
            "name": "查询所有housing类型匹配",
            "params": {"status": "null", "page": 1, "pageSize": 10, "matchType": "housing"}
        },
        {
            "name": "查询pending状态的housing匹配",
            "params": {"status": "pending", "page": 1, "pageSize": 5, "matchType": "housing"}
        },
        {
            "name": "查询activity类型匹配",
            "params": {"status": "null", "page": 1, "pageSize": 10, "matchType": "activity"}
        },
        {
            "name": "查询accepted状态的activity匹配",
            "params": {"status": "accepted", "page": 1, "pageSize": 5, "matchType": "activity"}
        },
        {
            "name": "查询第二页数据",
            "params": {"status": "null", "page": 2, "pageSize": 5, "matchType": "housing"}
        }
    ]
    
    print("开始全面测试匹配API...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        
        # 构建查询参数
        params = test_case['params']
        print(f"查询参数: {params}")
        
        # 发送请求
        response = client.get("/api/v1/matches", params=params)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 请求成功")
            
            # 检查响应结构
            if 'data' in data and 'matches' in data['data']:
                matches = data['data']['matches']
                print(f"返回匹配记录数: {len(matches)}")
                
                # 验证筛选条件
                if matches:
                    print("匹配记录验证:")
                    for j, match in enumerate(matches[:3]):  # 只检查前3条
                        match_type = match.get('match_type')
                        status = match.get('status')
                        print(f"  记录{j+1}: ID={match.get('id')}, 类型={match_type}, 状态={status}")
                        
                        # 验证类型筛选
                        if params.get('matchType') and match_type != params['matchType']:
                            print(f"    ❌ 类型筛选错误: 期望{params['matchType']}, 实际{match_type}")
                        
                        # 验证状态筛选
                        if params.get('status') and params['status'] != 'null' and status != params['status']:
                            print(f"    ❌ 状态筛选错误: 期望{params['status']}, 实际{status}")
                
                # 显示分页信息
                pagination_info = {
                    "total": data['data'].get('total'),
                    "page": data['data'].get('page'),
                    "pageSize": data['data'].get('pageSize'),
                    "totalPages": data['data'].get('totalPages')
                }
                print(f"分页信息: {pagination_info}")
                
            else:
                print("❌ 响应结构不正确，缺少matches字段")
                print(f"实际响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 请求失败: {response.text}")
        
        print("-" * 40)
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_matches_with_different_params()