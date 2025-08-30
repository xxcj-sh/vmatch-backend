-- 为测试用户 test_user_001 生成匹配测试数据
-- 支持接口查询: GET /api/v1/matches?status=null&page=1&pageSize=10&matchType=activity

-- 首先确保测试用户存在
INSERT OR IGNORE INTO users (
    username, email, phone, nickname, gender, age, location, bio, 
    avatar_url, is_active, created_at, updated_at
) VALUES 
('test_user_001', 'test_user_001@test.com', '13800000001', '测试用户001', 'male', 25, '北京市', '这是测试用户001', 'https://example.com/avatar1.jpg', 1, datetime('now'), datetime('now')),
('test_user_002', 'test_user_002@test.com', '13800000002', '测试用户002', 'female', 23, '北京市', '这是测试用户002', 'https://example.com/avatar2.jpg', 1, datetime('now'), datetime('now')),
('test_user_003', 'test_user_003@test.com', '13800000003', '测试用户003', 'male', 27, '北京市', '这是测试用户003', 'https://example.com/avatar3.jpg', 1, datetime('now'), datetime('now')),
('test_user_004', 'test_user_004@test.com', '13800000004', '测试用户004', 'female', 24, '北京市', '这是测试用户004', 'https://example.com/avatar4.jpg', 1, datetime('now'), datetime('now')),
('test_user_005', 'test_user_005@test.com', '13800000005', '测试用户005', 'male', 26, '北京市', '这是测试用户005', 'https://example.com/avatar5.jpg', 1, datetime('now'), datetime('now'));

-- 清理现有的测试匹配数据
DELETE FROM matches WHERE 
    user1_id IN (SELECT id FROM users WHERE username LIKE 'test_user_%') OR
    user2_id IN (SELECT id FROM users WHERE username LIKE 'test_user_%');

-- 插入测试匹配数据 (activity 类型)
INSERT INTO matches (
    user1_id, user2_id, match_type, status, activity_id, activity_name, 
    activity_location, activity_time, message, created_at, updated_at, expires_at
) VALUES 
-- pending 状态的匹配
((SELECT id FROM users WHERE username = 'test_user_001'), (SELECT id FROM users WHERE username = 'test_user_002'), 'activity', 'pending', 'activity_1001', '周末户外徒步', '北京市海淀区香山公园', datetime('now', '+3 days'), '一起去香山徒步吧！', datetime('now', '-1 day'), datetime('now', '-1 day'), datetime('now', '+6 days')),
((SELECT id FROM users WHERE username = 'test_user_003'), (SELECT id FROM users WHERE username = 'test_user_001'), 'activity', 'pending', 'activity_1002', '咖啡厅读书会', '北京市朝阳区三里屯', datetime('now', '+2 days'), '想找个人一起读书', datetime('now', '-2 hours'), datetime('now', '-2 hours'), datetime('now', '+6 days')),
((SELECT id FROM users WHERE username = 'test_user_001'), (SELECT id FROM users WHERE username = 'test_user_004'), 'activity', 'pending', 'activity_1003', '电影院看新片', '北京市西城区西单大悦城', datetime('now', '+1 day'), NULL, datetime('now', '-5 hours'), datetime('now', '-5 hours'), datetime('now', '+6 days')),

-- accepted 状态的匹配
((SELECT id FROM users WHERE username = 'test_user_001'), (SELECT id FROM users WHERE username = 'test_user_005'), 'activity', 'accepted', 'activity_1004', '健身房运动', '北京市朝阳区健身中心', datetime('now', '+4 days'), '一起健身！', datetime('now', '-3 days'), datetime('now', '-2 days'), datetime('now', '+4 days')),
((SELECT id FROM users WHERE username = 'test_user_002'), (SELECT id FROM users WHERE username = 'test_user_001'), 'activity', 'accepted', 'activity_1005', '美术馆参观', '北京市东城区中国美术馆', datetime('now', '+5 days'), '对艺术很感兴趣', datetime('now', '-4 days'), datetime('now', '-3 days'), datetime('now', '+3 days')),
((SELECT id FROM users WHERE username = 'test_user_001'), (SELECT id FROM users WHERE username = 'test_user_003'), 'activity', 'accepted', 'activity_1006', '公园散步', '北京市海淀区圆明园', datetime('now', '+2 days'), '天气不错，一起散步', datetime('now', '-1 day'), datetime('now', '-12 hours'), datetime('now', '+6 days')),

-- rejected 状态的匹配
((SELECT id FROM users WHERE username = 'test_user_004'), (SELECT id FROM users WHERE username = 'test_user_001'), 'activity', 'rejected', 'activity_1007', '音乐会欣赏', '北京市西城区国家大剧院', datetime('now', '+7 days'), '古典音乐爱好者', datetime('now', '-5 days'), datetime('now', '-4 days'), datetime('now', '+2 days')),
((SELECT id FROM users WHERE username = 'test_user_001'), (SELECT id FROM users WHERE username = 'test_user_005'), 'activity', 'rejected', 'activity_1008', '博物馆参观', '北京市东城区故宫博物院', datetime('now', '+3 days'), NULL, datetime('now', '-6 days'), datetime('now', '-5 days'), datetime('now', '+1 day')),

-- expired 状态的匹配
((SELECT id FROM users WHERE username = 'test_user_003'), (SELECT id FROM users WHERE username = 'test_user_001'), 'activity', 'expired', 'activity_1009', '图书馆学习', '北京市海淀区国家图书馆', datetime('now', '-1 day'), '一起学习提升', datetime('now', '-8 days'), datetime('now', '-8 days'), datetime('now', '-1 day')),
((SELECT id FROM users WHERE username = 'test_user_001'), (SELECT id FROM users WHERE username = 'test_user_002'), 'activity', 'expired', 'activity_1010', '购物中心逛街', '北京市朝阳区国贸商城', datetime('now', '-2 days'), '周末逛街', datetime('now', '-10 days'), datetime('now', '-10 days'), datetime('now', '-3 days')),

-- 更多测试数据
((SELECT id FROM users WHERE username = 'test_user_005'), (SELECT id FROM users WHERE username = 'test_user_001'), 'activity', 'pending', 'activity_1011', '羽毛球运动', '北京市朝阳区体育馆', datetime('now', '+6 days'), '找球友一起打球', datetime('now', '-30 minutes'), datetime('now', '-30 minutes'), datetime('now', '+6 days')),
((SELECT id FROM users WHERE username = 'test_user_001'), (SELECT id FROM users WHERE username = 'test_user_004'), 'activity', 'accepted', 'activity_1012', '餐厅聚餐', '北京市西城区王府井', datetime('now', '+1 day'), '尝试新餐厅', datetime('now', '-2 days'), datetime('now', '-1 day'), datetime('now', '+5 days')),
((SELECT id FROM users WHERE username = 'test_user_002'), (SELECT id FROM users WHERE username = 'test_user_001'), 'activity', 'pending', 'activity_1013', '公园跑步', '北京市朝阳区奥林匹克森林公园', datetime('now', '+3 days'), '晨跑爱好者', datetime('now', '-4 hours'), datetime('now', '-4 hours'), datetime('now', '+6 days')),
((SELECT id FROM users WHERE username = 'test_user_001'), (SELECT id FROM users WHERE username = 'test_user_003'), 'activity', 'rejected', 'activity_1014', 'KTV唱歌', '北京市海淀区中关村', datetime('now', '+2 days'), NULL, datetime('now', '-7 days'), datetime('now', '-6 days'), datetime('now', '+0 days')),
((SELECT id FROM users WHERE username = 'test_user_004'), (SELECT id FROM users WHERE username = 'test_user_001'), 'activity', 'expired', 'activity_1015', '游泳健身', '北京市东城区游泳馆', datetime('now', '-3 days'), '游泳爱好者', datetime('now', '-12 days'), datetime('now', '-12 days'), datetime('now', '-5 days'));

-- 查询验证数据
SELECT 
    m.id,
    u1.username as user1,
    u2.username as user2,
    m.match_type,
    m.status,
    m.activity_name,
    m.activity_location,
    m.activity_time,
    m.created_at,
    m.expires_at
FROM matches m
JOIN users u1 ON m.user1_id = u1.id
JOIN users u2 ON m.user2_id = u2.id
WHERE (u1.username = 'test_user_001' OR u2.username = 'test_user_001')
    AND m.match_type = 'activity'
ORDER BY m.created_at DESC;