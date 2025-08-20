#!/usr/bin/env python3
"""
生成固定测试房源数据的工具
确保每个房源ID都有对应的测试样本，避免展示问题
"""

import json
import os
import sys
from typing import Dict, List, Any
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# 导入测试数据生成器
from app.utils.test_data_generator import TestDataGenerator

# 预定义的固定房源ID列表，确保一致性
FIXED_HOUSING_IDS = [
    "house_test_001", "house_test_002", "house_test_003", 
    "house_test_004", "house_test_005", "house_test_006",
    "house_test_007", "house_test_008", "house_test_009", 
    "house_test_010"
]

# 预定义的测试房源数据模板
HOUSING_TEMPLATES = [
    {
        "title": "温馨一居室 · 近地铁",
        "price": 2800,
        "area": 45,
        "location": "朝阳区 · 望京",
        "features": ["近地铁", "精装修", "拎包入住"],
        "description": "温馨舒适的一居室，距离地铁14号线仅500米，周边配套齐全，拎包即可入住。"
    },
    {
        "title": "阳光两居室 · 业主直租",
        "price": 4500,
        "area": 75,
        "location": "海淀区 · 五道口",
        "features": ["业主直租", "南北通透", "学区房"],
        "description": "南北通透的两居室，采光极佳，业主直租无中介费，周边有多所知名高校。"
    },
    {
        "title": "精装公寓 · 拎包入住",
        "price": 3200,
        "area": 55,
        "location": "西城区 · 金融街",
        "features": ["精装修", "家电齐全", "近商圈"],
        "description": "高端精装公寓，家电家具齐全，步行可达金融街各大银行总部，适合白领居住。"
    },
    {
        "title": "经济单间 · 学生优选",
        "price": 1800,
        "area": 25,
        "location": "海淀区 · 中关村",
        "features": ["学生优选", "近高校", "交通便利"],
        "description": "经济实惠的单间，适合学生或刚毕业的年轻人，周边有多条公交线路。"
    },
    {
        "title": "豪华三居 · 全配齐",
        "price": 6800,
        "area": 110,
        "location": "朝阳区 · CBD",
        "features": ["豪华装修", "全套家电", "近CBD"],
        "description": "豪华装修三居室，全套品牌家电，适合家庭居住，步行可达国贸CBD核心区。"
    }
]

def generate_fixed_housing_data() -> Dict[str, Any]:
    """生成固定测试房源数据"""
    
    # 生成测试用户（确保房东用户存在）
    test_users = []
    test_user_ids = ["user_001", "user_002", "user_003", "user_004", "user_005"]
    
    for user_id in test_user_ids:
        user = TestDataGenerator.generate_user()
        user["id"] = user_id
        user["nickName"] = f"房东{user_id[-3:]}"
        user["role"] = "landlord"
        test_users.append(user)
    
    # 生成固定房源数据
    housing_cards = []
    
    for i, (house_id, template) in enumerate(zip(FIXED_HOUSING_IDS, HOUSING_TEMPLATES)):
        # 使用固定的房东用户
        landlord_user_id = test_user_ids[i % len(test_user_ids)]
        
        # 生成基础卡片数据
        card = TestDataGenerator.generate_card(
            card_id=f"card_{house_id}",
            match_type="housing",
            user_role="seeker",
            landlord_user_id=landlord_user_id
        )
        
        # 更新房源信息为固定模板
        house_info = card["houseInfo"]
        house_info.update({
            "id": house_id,
            "title": template["title"],
            "price": template["price"],
            "area": template["area"],
            "location": template["location"],
            "features": template["features"],
            "description": template["description"],
            "images": [
                "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800",
                "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"
            ],
            "videoUrl": "https://cdn.pixabay.com/video/2024/02/03/199109-909564730_tiny.mp4"
        })
        
        # 更新房东信息
        landlord_info = card["landlordInfo"]
        landlord_info.update({
            "id": landlord_user_id,
            "name": f"房东{landlord_user_id[-3:]}",
            "verified": True,
            "responseRate": "98%",
            "bio": f"我是专业房东{landlord_user_id[-3:]}，拥有多套房源，致力于为租客提供舒适安心的居住环境。"
        })
        
        housing_cards.append(card)
    
    # 生成匹配记录
    matches = []
    for i, card in enumerate(housing_cards):
        match = TestDataGenerator.generate_match(
            match_id=f"match_{card['id']}",
            user_id="user_test_seeker",
            card_id=card["id"]
        )
        match["type"] = "housing"
        matches.append(match)
    
    return {
        "metadata": {
            "generatedAt": datetime.now().isoformat(),
            "version": "1.0",
            "description": "固定测试房源数据，确保ID与样本对应"
        },
        "testUsers": test_users,
        "housingCards": housing_cards,
        "matches": matches,
        "apiEndpoints": {
            "getHousingCards": "GET /api/v1/match/cards?matchType=housing&userRole=seeker",
            "getUserProfile": "GET /api/v1/user/profile?userId={user_id}",
            "getMatchDetail": "GET /api/v1/match/detail/{match_id}"
        }
    }

def main():
    """主函数：生成并保存固定测试数据"""
    
    print("🏠 生成固定测试房源数据...")
    
    # 生成数据
    data = generate_fixed_housing_data()
    
    # 保存到文件
    output_file = "fixed_housing_test_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 固定测试数据已生成并保存到: {output_file}")
    
    # 验证数据完整性
    print("\n📊 数据概览:")
    print(f"   测试用户: {len(data['testUsers'])} 个")
    print(f"   房源卡片: {len(data['housingCards'])} 个")
    print(f"   匹配记录: {len(data['matches'])} 个")
    
    print(f"\n🏠 固定房源ID列表:")
    for card in data['housingCards']:
        house_id = card['houseInfo']['id']
        title = card['houseInfo']['title']
        landlord = card['landlordInfo']['id']
        print(f"   {house_id}: {title} (房东: {landlord})")
    
    print(f"\n🔗 测试API端点:")
    for card in data['housingCards']:
        card_id = card['id']
        house_id = card['houseInfo']['id']
        landlord_id = card['landlordInfo']['id']
        print(f"   卡片: http://localhost:8000/api/v1/match/cards?matchType=housing&userRole=seeker")
        print(f"   房源: {house_id} -> 卡片: {card_id}")
        print(f"   房东: http://localhost:8000/api/v1/user/profile?userId={landlord_id}")
        break  # 只显示第一个示例

if __name__ == "__main__":
    main()