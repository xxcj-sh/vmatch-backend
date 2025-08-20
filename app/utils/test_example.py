"""
测试示例
演示如何使用测试工具和测试数据生成器
"""
from app.utils.test_utils import test_utils
from app.utils.test_data_generator import test_data_generator
import json

def print_json(data):
    """格式化打印JSON数据"""
    print(json.dumps(data, ensure_ascii=False, indent=2))

def run_examples():
    """运行测试示例"""
    print("\n===== 微信小程序API测试工具示例 =====\n")
    
    # 检查测试模式
    print(f"当前测试模式: {'启用' if test_utils.is_test_mode() else '禁用'}")
    
    # 启用测试模式
    test_utils.enable_test_mode()
    
    print("\n----- 生成用户数据示例 -----")
    user = test_utils.generate_user_data()
    print_json(user)
    
    print("\n----- 生成卡片数据示例 -----")
    card = test_utils.generate_card_data()
    print_json(card)
    
    print("\n----- 生成匹配数据示例 -----")
    match = test_utils.generate_match_data(user_id=user["id"], card_id=card["id"])
    print_json(match)
    
    print("\n----- 生成消息数据示例 -----")
    message = test_utils.generate_message_data(match_id=match["id"], sender_id=user["id"])
    print_json(message)
    
    print("\n----- 生成会员数据示例 -----")
    membership = test_utils.generate_membership_data(user_id=user["id"])
    print_json(membership)
    
    print("\n----- 生成支付数据示例 -----")
    payment = test_utils.generate_payment_data(user_id=user["id"])
    print_json(payment)
    
    # 添加固定测试用户示例
    print("\n----- 固定测试用户示例 -----")
    fixed_user = test_utils.get_fixed_test_user()
    print_json(fixed_user)

    print("\n----- 固定测试用户登录信息 -----")
    print(f"手机号: {fixed_user['phone']}")
    print(f"验证码: 123456")
    print(f"Token: {test_utils.get_fixed_test_token()}")
    print(f"Authorization: {test_utils.get_fixed_test_headers()['Authorization']}")
    
    print("\n----- 模拟API响应示例 -----")
    
    # 登录API
    login_response = test_data_generator.mock_api_response(
        "/api/v1/auth/login", 
        "POST", 
        {"code": "test_code", "userInfo": {"nickName": "测试用户", "avatarUrl": "https://example.com/avatar.jpg"}}
    )
    print("登录API响应:")
    print_json(login_response)
    
    # 获取用户信息API
    user_info_response = test_data_generator.mock_api_response("/api/v1/user/info", "GET")
    print("\n获取用户信息API响应:")
    print_json(user_info_response)
    
    # 获取匹配卡片API
    match_cards_response = test_data_generator.mock_api_response(
        "/api/v1/match/cards", 
        "GET", 
        {"type": "dating", "userRole": "seeker", "page": 1, "pageSize": 3}
    )
    print("\n获取匹配卡片API响应:")
    print_json(match_cards_response)
    
    # 发送消息API
    send_message_response = test_data_generator.mock_api_response(
        "/api/v1/chat/send", 
        "POST", 
        {"matchId": match["id"], "content": "你好，这是一条测试消息", "type": "text"}
    )
    print("\n发送消息API响应:")
    print_json(send_message_response)
    
    print("\n===== 示例结束 =====")

if __name__ == "__main__":
    run_examples()