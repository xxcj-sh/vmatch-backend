#!/usr/bin/env python3
"""
测试匹配API端点
"""

import requests
import json

def test_matches_api():
    """测试匹配API"""
    
    base_url = "http://localhost:8001/api/v1"
    
    # 测试查询参数
    test_cases = [
        {
            "name": "查询所有housing类型匹配",
            "url": f"{base_url}/matches?status=null&page=1&pageSize=10&matchType=housing",
        },
        {
            "name": "查询pending状态的housing匹配",
            "url": f"{base_url}/matches?status=pending&page=1&pageSize=5&matchType=housing",
        },
        {
            "name": "查询activity类型匹配",
            "url": f"{base_url}/matches?status=null&page=1&pageSize=10&matchType=activity",
        },
        {
            "name": "查询第二页数据",
            "url": f"{base_url}/matches?status=null&page=2&pageSize=5&matchType=housing",
        }
    ]
    
    print("开始测试匹配API...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"URL: {test_case['url']}")
        
        try:
            # 发送GET请求
            response = requests.get(test_case['url'])
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 请求成功")
                
                # 检查响应结构
                if 'data' in data and 'matches' in data['data']:
                    matches = data['data']['matches']
                    print(f"返回匹配记录数: {len(matches)}")
                    
                    if matches:
                        print("前3条记录:")
                        for j, match in enumerate(matches[:3]):
                            print(f"  {j+1}. ID:{match.get('id')} 状态:{match.get('status')} 类型:{match.get('match_type')}")
                    
                    # 显示分页信息
                    if 'total' in data['data']:
                        print(f"总记录数: {data['data']['total']}")
                    if 'page' in data['data']:
                        print(f"当前页: {data['data']['page']}")
                    if 'pageSize' in data['data']:
                        print(f"页大小: {data['data']['pageSize']}")
                else:
                    print("❌ 响应结构不正确，缺少 matches 字段")
                    print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                
            else:
                print(f"❌ 请求失败")
                print(f"响应内容: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 连接失败 - 请确保API服务器正在运行")
        except Exception as e:
            print(f"❌ 请求出错: {str(e)}")
        
        print("-" * 40)
    
    print(f"\n测试完成！")

if __name__ == "__main__":
    test_matches_api()