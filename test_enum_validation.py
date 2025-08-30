#!/usr/bin/env python3
"""
测试枚举值验证
"""

from fastapi.testclient import TestClient
from app.main import app
from app.models.enums import *
import json

client = TestClient(app)

def test_matches_enum_values():
    """测试匹配数据的枚举值"""
    
    print("测试匹配数据枚举值...")
    print("=" * 60)
    
    # 测试不同类型的匹配查询
    test_cases = [
        {
            "name": "活动匹配数据",
            "params": {"status": "null", "page": 1, "pageSize": 5, "matchType": "activity"}
        },
        {
            "name": "房源匹配数据", 
            "params": {"status": "null", "page": 1, "pageSize": 5, "matchType": "housing"}
        },
        {
            "name": "交友匹配数据",
            "params": {"status": "null", "page": 1, "pageSize": 5, "matchType": "dating"}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        
        # 发送请求
        response = client.get("/api/v1/matches", params=test_case['params'])
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('data', {}).get('matches', [])
            
            if matches:
                match = matches[0]  # 检查第一条记录
                print(f"✅ 获取到 {len(matches)} 条匹配记录")
                
                # 验证基础字段
                match_type = match.get('match_type')
                status = match.get('status')
                
                print(f"匹配类型: {match_type}")
                print(f"匹配状态: {status}")
                
                # 验证枚举值
                if match_type in [mt.value for mt in MatchType]:
                    print("✅ 匹配类型符合枚举值")
                else:
                    print(f"❌ 匹配类型不符合枚举值: {match_type}")
                
                if status in [ms.value for ms in MatchStatus]:
                    print("✅ 匹配状态符合枚举值")
                else:
                    print(f"❌ 匹配状态不符合枚举值: {status}")
                
                # 根据类型验证特定字段
                if match_type == "activity":
                    validate_activity_match(match)
                elif match_type == "housing":
                    validate_housing_match(match)
                elif match_type == "dating":
                    validate_dating_match(match)
                    
            else:
                print("❌ 未获取到匹配记录")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        
        print("-" * 40)

def validate_activity_match(match):
    """验证活动匹配数据"""
    print("验证活动匹配特定字段:")
    
    activity_type = match.get('activity_type')
    skill_level = match.get('skill_level')
    group_size = match.get('group_size')
    budget = match.get('budget')
    
    # 验证活动类型
    if activity_type and activity_type in [at.value for at in ActivityType]:
        print(f"✅ 活动类型符合枚举值: {activity_type}")
    else:
        print(f"❌ 活动类型不符合枚举值: {activity_type}")
    
    # 验证技能水平
    if skill_level and skill_level in [sl.value for sl in SkillLevel]:
        print(f"✅ 技能水平符合枚举值: {skill_level}")
    else:
        print(f"❌ 技能水平不符合枚举值: {skill_level}")
    
    # 验证团队规模
    if group_size and group_size in [gs.value for gs in GroupSize]:
        print(f"✅ 团队规模符合枚举值: {group_size}")
    else:
        print(f"❌ 团队规模不符合枚举值: {group_size}")
    
    # 验证预算
    if budget and budget in [ab.value for ab in ActivityBudget]:
        print(f"✅ 活动预算符合枚举值: {budget}")
    else:
        print(f"❌ 活动预算不符合枚举值: {budget}")

def validate_housing_match(match):
    """验证房源匹配数据"""
    print("验证房源匹配特定字段:")
    
    house_type = match.get('house_type')
    budget_range = match.get('budget_range')
    decoration = match.get('decoration')
    facilities = match.get('facilities', [])
    
    # 验证房屋类型
    if house_type and house_type in [ht.value for ht in HouseType]:
        print(f"✅ 房屋类型符合枚举值: {house_type}")
    else:
        print(f"❌ 房屋类型不符合枚举值: {house_type}")
    
    # 验证预算范围
    if budget_range and budget_range in [br.value for br in BudgetRange]:
        print(f"✅ 预算范围符合枚举值: {budget_range}")
    else:
        print(f"❌ 预算范围不符合枚举值: {budget_range}")
    
    # 验证装修程度
    if decoration and decoration in [dl.value for dl in DecorationLevel]:
        print(f"✅ 装修程度符合枚举值: {decoration}")
    else:
        print(f"❌ 装修程度不符合枚举值: {decoration}")
    
    # 验证设施
    facility_values = [f.value for f in Facility]
    valid_facilities = all(facility in facility_values for facility in facilities)
    if valid_facilities:
        print(f"✅ 房屋设施符合枚举值: {facilities}")
    else:
        invalid_facilities = [f for f in facilities if f not in facility_values]
        print(f"❌ 房屋设施包含无效值: {invalid_facilities}")

def validate_dating_match(match):
    """验证交友匹配数据"""
    print("验证交友匹配特定字段:")
    
    education = match.get('education')
    interests = match.get('interests', [])
    income_range = match.get('income_range')
    height_range = match.get('height_range')
    marital_status = match.get('marital_status')
    work_industry = match.get('work_industry')
    
    # 验证教育程度
    if education and education in [e.value for e in Education]:
        print(f"✅ 教育程度符合枚举值: {education}")
    else:
        print(f"❌ 教育程度不符合枚举值: {education}")
    
    # 验证兴趣爱好
    interest_values = [i.value for i in Interest]
    valid_interests = all(interest in interest_values for interest in interests)
    if valid_interests:
        print(f"✅ 兴趣爱好符合枚举值: {interests}")
    else:
        invalid_interests = [i for i in interests if i not in interest_values]
        print(f"❌ 兴趣爱好包含无效值: {invalid_interests}")
    
    # 验证收入范围
    if income_range and income_range in [ir.value for ir in IncomeRange]:
        print(f"✅ 收入范围符合枚举值: {income_range}")
    else:
        print(f"❌ 收入范围不符合枚举值: {income_range}")
    
    # 验证身高范围
    if height_range and height_range in [hr.value for hr in HeightRange]:
        print(f"✅ 身高范围符合枚举值: {height_range}")
    else:
        print(f"❌ 身高范围不符合枚举值: {height_range}")
    
    # 验证婚姻状况
    if marital_status and marital_status in [ms.value for ms in MaritalStatus]:
        print(f"✅ 婚姻状况符合枚举值: {marital_status}")
    else:
        print(f"❌ 婚姻状况不符合枚举值: {marital_status}")
    
    # 验证工作行业
    if work_industry and work_industry in [wi.value for wi in WorkIndustry]:
        print(f"✅ 工作行业符合枚举值: {work_industry}")
    else:
        print(f"❌ 工作行业不符合枚举值: {work_industry}")

def test_enum_completeness():
    """测试枚举值完整性"""
    print("\n测试枚举值完整性...")
    print("=" * 60)
    
    # 检查主要枚举类是否包含预期的值
    enum_tests = [
        {
            "name": "地区枚举",
            "enum_class": Region,
            "expected_values": ["北京", "上海", "广州", "深圳", "杭州", "成都", "其他"]
        },
        {
            "name": "教育程度枚举",
            "enum_class": Education,
            "expected_values": ["高中", "大专", "本科", "硕士", "博士", "其他"]
        },
        {
            "name": "房屋类型枚举",
            "enum_class": HouseType,
            "expected_values": ["整租", "合租", "主卧", "次卧", "公寓", "别墅"]
        },
        {
            "name": "活动类型枚举",
            "enum_class": ActivityType,
            "expected_values": ["运动健身", "文化艺术", "户外探险", "美食品鉴", "学习交流", "娱乐休闲", "其他"]
        }
    ]
    
    for test in enum_tests:
        print(f"\n检查 {test['name']}:")
        enum_values = [item.value for item in test['enum_class']]
        
        missing_values = []
        for expected in test['expected_values']:
            if expected not in enum_values:
                missing_values.append(expected)
        
        if not missing_values:
            print(f"✅ {test['name']} 包含所有预期值")
            print(f"   值: {enum_values}")
        else:
            print(f"❌ {test['name']} 缺少值: {missing_values}")
            print(f"   当前值: {enum_values}")

if __name__ == "__main__":
    test_matches_enum_values()
    test_enum_completeness()
    print("\n测试完成！")