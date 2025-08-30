#!/usr/bin/env python3
"""
测试API接口返回的数据是否符合枚举值要求
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app
from app.models.enums import *
import json

client = TestClient(app)

def test_api_endpoint(endpoint: str, params: dict, test_name: str):
    """测试API端点"""
    print(f"\n🔍 测试: {test_name}")
    print(f"请求: GET {endpoint}")
    print(f"参数: {params}")
    
    response = client.get(endpoint, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 响应状态: {response.status_code}")
        
        # 检查响应结构
        if 'data' in data and 'matches' in data['data']:
            matches = data['data']['matches']
            total = data['data'].get('total', 0)
            page = data['data'].get('page', 1)
            page_size = data['data'].get('pageSize', 10)
            
            print(f"📊 数据统计: 总数={total}, 当前页={page}, 页大小={page_size}, 返回={len(matches)}")
            
            if matches:
                return validate_matches_data(matches, params.get('matchType'))
            else:
                print("⚠️  未返回匹配数据")
                return False
        else:
            print("❌ 响应结构不正确，缺少 data.matches 字段")
            return False
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return False

def validate_matches_data(matches: list, match_type: str):
    """验证匹配数据是否符合枚举值"""
    print(f"🔍 验证 {len(matches)} 条匹配记录...")
    
    valid_count = 0
    invalid_items = []
    
    for i, match in enumerate(matches):
        is_valid = True
        errors = []
        
        # 验证基础字段
        match_type_val = match.get('match_type')
        status_val = match.get('status')
        
        # 检查匹配类型
        if match_type_val not in [mt.value for mt in MatchType]:
            is_valid = False
            errors.append(f"无效的匹配类型: {match_type_val}")
        
        # 检查匹配状态
        if status_val not in [ms.value for ms in MatchStatus]:
            is_valid = False
            errors.append(f"无效的匹配状态: {status_val}")
        
        # 根据匹配类型验证特定字段
        if match_type == "activity":
            is_valid &= validate_activity_fields(match, errors)
        elif match_type == "housing":
            is_valid &= validate_housing_fields(match, errors)
        elif match_type == "dating":
            is_valid &= validate_dating_fields(match, errors)
        
        if is_valid:
            valid_count += 1
        else:
            invalid_items.append({
                'index': i,
                'match_id': match.get('match_id', 'unknown'),
                'errors': errors
            })
    
    # 输出验证结果
    print(f"✅ 有效记录: {valid_count}/{len(matches)}")
    
    if invalid_items:
        print(f"❌ 无效记录: {len(invalid_items)}")
        for item in invalid_items[:3]:  # 只显示前3个错误
            print(f"  记录 {item['index']}: {item['match_id']}")
            for error in item['errors']:
                print(f"    - {error}")
        if len(invalid_items) > 3:
            print(f"  ... 还有 {len(invalid_items) - 3} 个错误")
    
    return len(invalid_items) == 0

def validate_activity_fields(match: dict, errors: list) -> bool:
    """验证活动匹配字段"""
    is_valid = True
    
    # 验证活动类型
    activity_type = match.get('activity_type')
    if activity_type and activity_type not in [at.value for at in ActivityType]:
        is_valid = False
        errors.append(f"无效的活动类型: {activity_type}")
    
    # 验证技能水平
    skill_level = match.get('skill_level')
    if skill_level and skill_level not in [sl.value for sl in SkillLevel]:
        is_valid = False
        errors.append(f"无效的技能水平: {skill_level}")
    
    # 验证团队规模
    group_size = match.get('group_size')
    if group_size and group_size not in [gs.value for gs in GroupSize]:
        is_valid = False
        errors.append(f"无效的团队规模: {group_size}")
    
    # 验证预算
    budget = match.get('budget')
    if budget and budget not in [ab.value for ab in ActivityBudget]:
        is_valid = False
        errors.append(f"无效的活动预算: {budget}")
    
    return is_valid

def validate_housing_fields(match: dict, errors: list) -> bool:
    """验证房源匹配字段"""
    is_valid = True
    
    # 验证房屋类型
    house_type = match.get('house_type')
    if house_type and house_type not in [ht.value for ht in HouseType]:
        is_valid = False
        errors.append(f"无效的房屋类型: {house_type}")
    
    # 验证预算范围
    budget_range = match.get('budget_range')
    if budget_range and budget_range not in [br.value for br in BudgetRange]:
        is_valid = False
        errors.append(f"无效的预算范围: {budget_range}")
    
    # 验证装修程度
    decoration = match.get('decoration')
    if decoration and decoration not in [dl.value for dl in DecorationLevel]:
        is_valid = False
        errors.append(f"无效的装修程度: {decoration}")
    
    # 验证设施
    facilities = match.get('facilities', [])
    if facilities:
        facility_values = [f.value for f in Facility]
        invalid_facilities = [f for f in facilities if f not in facility_values]
        if invalid_facilities:
            is_valid = False
            errors.append(f"无效的房屋设施: {invalid_facilities}")
    
    return is_valid

def validate_dating_fields(match: dict, errors: list) -> bool:
    """验证交友匹配字段"""
    is_valid = True
    
    # 验证教育程度
    education = match.get('education')
    if education and education not in [e.value for e in Education]:
        is_valid = False
        errors.append(f"无效的教育程度: {education}")
    
    # 验证兴趣爱好
    interests = match.get('interests', [])
    if interests:
        interest_values = [i.value for i in Interest]
        invalid_interests = [i for i in interests if i not in interest_values]
        if invalid_interests:
            is_valid = False
            errors.append(f"无效的兴趣爱好: {invalid_interests}")
    
    # 验证收入范围
    income_range = match.get('income_range')
    if income_range and income_range not in [ir.value for ir in IncomeRange]:
        is_valid = False
        errors.append(f"无效的收入范围: {income_range}")
    
    # 验证身高范围
    height_range = match.get('height_range')
    if height_range and height_range not in [hr.value for hr in HeightRange]:
        is_valid = False
        errors.append(f"无效的身高范围: {height_range}")
    
    # 验证婚姻状况
    marital_status = match.get('marital_status')
    if marital_status and marital_status not in [ms.value for ms in MaritalStatus]:
        is_valid = False
        errors.append(f"无效的婚姻状况: {marital_status}")
    
    # 验证工作行业
    work_industry = match.get('work_industry')
    if work_industry and work_industry not in [wi.value for wi in WorkIndustry]:
        is_valid = False
        errors.append(f"无效的工作行业: {work_industry}")
    
    return is_valid

def main():
    """主测试函数"""
    print("🚀 开始测试API接口的枚举值合规性...")
    print("=" * 80)
    
    # 测试用例
    test_cases = [
        {
            "name": "活动匹配 - 全部状态",
            "endpoint": "/api/v1/matches",
            "params": {"status": "null", "page": 1, "pageSize": 10, "matchType": "activity"}
        },
        {
            "name": "活动匹配 - 待处理状态",
            "endpoint": "/api/v1/matches",
            "params": {"status": "pending", "page": 1, "pageSize": 5, "matchType": "activity"}
        },
        {
            "name": "房源匹配 - 全部状态",
            "endpoint": "/api/v1/matches",
            "params": {"status": "null", "page": 1, "pageSize": 10, "matchType": "housing"}
        },
        {
            "name": "房源匹配 - 已接受状态",
            "endpoint": "/api/v1/matches",
            "params": {"status": "accepted", "page": 1, "pageSize": 5, "matchType": "housing"}
        },
        {
            "name": "交友匹配 - 全部状态",
            "endpoint": "/api/v1/matches",
            "params": {"status": "null", "page": 1, "pageSize": 10, "matchType": "dating"}
        },
        {
            "name": "交友匹配 - 已拒绝状态",
            "endpoint": "/api/v1/matches",
            "params": {"status": "rejected", "page": 1, "pageSize": 5, "matchType": "dating"}
        }
    ]
    
    # 执行测试
    passed_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 测试 {i}/{total_tests}")
        success = test_api_endpoint(
            test_case["endpoint"],
            test_case["params"],
            test_case["name"]
        )
        
        if success:
            passed_tests += 1
            print("✅ 测试通过")
        else:
            print("❌ 测试失败")
        
        print("-" * 60)
    
    # 输出总结
    print(f"\n📊 测试总结:")
    print(f"通过: {passed_tests}/{total_tests}")
    print(f"失败: {total_tests - passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！API返回的数据完全符合枚举值要求。")
    else:
        print("⚠️  部分测试失败，需要检查数据生成逻辑。")

if __name__ == "__main__":
    main()