# 测试数据设置指南

本文档说明如何为 `test_user_001` 生成测试数据以支持匹配API的测试。

## 概述

已为测试用户 `test_user_001` 生成了15条活动类型（activity）的匹配记录，涵盖了所有可能的匹配状态，用于测试以下API端点：

```
GET /api/v1/matches?status=null&page=1&pageSize=10&matchType=activity
```

## 生成的测试数据

### 测试用户
- `test_user_001` - 主要测试用户
- `test_user_002` - 测试用户2 (female, 23岁)
- `test_user_003` - 测试用户3 (male, 27岁)  
- `test_user_004` - 测试用户4 (female, 24岁)
- `test_user_005` - 测试用户5 (male, 26岁)

### 匹配记录统计
- **pending**: 5条记录 - 待处理的匹配请求
- **accepted**: 4条记录 - 已接受的匹配
- **rejected**: 3条记录 - 已拒绝的匹配  
- **expired**: 3条记录 - 已过期的匹配

### 活动类型示例
- 周末户外徒步 (香山公园)
- 咖啡厅读书会 (三里屯)
- 电影院看新片 (西单大悦城)
- 健身房运动 (朝阳区健身中心)
- 美术馆参观 (中国美术馆)
- 公园散步 (圆明园)
- 羽毛球运动 (朝阳区体育馆)
- 餐厅聚餐 (王府井)
- 公园跑步 (奥林匹克森林公园)
- 等等...

## 使用方法

### 1. 生成测试数据

运行以下脚本来生成测试数据：

```bash
cd scripts
python setup_test_data_sqlalchemy.py
```

### 2. 验证数据

运行验证脚本确认数据正确性：

```bash
cd scripts  
python test_matches_api.py
```

### 3. API测试

启动FastAPI服务器：

```bash
python -m app.main
```

然后使用以下API端点进行测试：

#### 基本查询
```http
GET /api/v1/matches?status=null&page=1&pageSize=10&matchType=activity
Authorization: Bearer <test_user_001_token>
```

#### 按状态筛选
```http
# 查询待处理匹配
GET /api/v1/matches?status=pending&page=1&pageSize=10&matchType=activity

# 查询已接受匹配  
GET /api/v1/matches?status=accepted&page=1&pageSize=10&matchType=activity

# 查询已拒绝匹配
GET /api/v1/matches?status=rejected&page=1&pageSize=10&matchType=activity

# 查询已过期匹配
GET /api/v1/matches?status=expired&page=1&pageSize=10&matchType=activity
```

#### 分页测试
```http
# 第一页，每页5条
GET /api/v1/matches?status=null&page=1&pageSize=5&matchType=activity

# 第二页，每页5条
GET /api/v1/matches?status=null&page=2&pageSize=5&matchType=activity

# 第三页，每页5条  
GET /api/v1/matches?status=null&page=3&pageSize=5&matchType=activity
```

## 预期响应格式

API应该返回以下格式的JSON响应：

```json
{
  "code": 200,
  "message": "success", 
  "data": [
    {
      "id": 1,
      "user1_id": 1,
      "user2_id": 2,
      "match_type": "activity",
      "status": "pending",
      "activity_id": "activity_1001",
      "activity_name": "周末户外徒步",
      "activity_location": "北京市海淀区香山公园",
      "activity_time": "2024-01-15T10:00:00",
      "message": "一起去香山徒步吧！",
      "created_at": "2024-01-12T08:00:00",
      "updated_at": "2024-01-12T08:00:00",
      "expires_at": "2024-01-19T08:00:00"
    }
  ],
  "total": 15,
  "page": 1,
  "pageSize": 10,
  "totalPages": 2
}
```

## 测试场景

### 1. 基本功能测试
- ✅ 查询所有activity类型匹配
- ✅ 分页功能正常工作
- ✅ 状态筛选功能正常

### 2. 边界条件测试  
- ✅ 查询不存在的页码
- ✅ 使用极大的pageSize值
- ✅ 查询不存在的状态

### 3. 数据完整性测试
- ✅ 返回的匹配记录包含完整字段
- ✅ 时间字段格式正确
- ✅ 用户关联正确

## 清理测试数据

如需清理测试数据，可以运行：

```python
from app.models.database import get_db
from app.models.match import Match
from app.models.user import User

db = next(get_db())

# 删除测试匹配记录
test_user_ids = [user.id for user in db.query(User).filter(User.username.like('test_user_%')).all()]
db.query(Match).filter(
    (Match.user1_id.in_(test_user_ids)) | (Match.user2_id.in_(test_user_ids))
).delete()

# 删除测试用户
db.query(User).filter(User.username.like('test_user_%')).delete()

db.commit()
db.close()
```

## 注意事项

1. **认证**: 根据实际的认证机制调整请求头中的Authorization字段
2. **端口**: 确保API服务器运行在正确的端口上
3. **数据库**: 确保数据库连接配置正确
4. **时区**: 注意时间字段的时区处理

## 故障排除

### 问题1: 数据库连接失败
**解决方案**: 检查数据库配置和连接字符串

### 问题2: API返回401未授权
**解决方案**: 检查认证token是否正确配置

### 问题3: 返回数据为空
**解决方案**: 确认测试数据已正确生成，运行验证脚本检查

### 问题4: 分页不正确
**解决方案**: 检查分页逻辑和总数计算

---

测试数据已准备就绪，可以开始API测试！🚀