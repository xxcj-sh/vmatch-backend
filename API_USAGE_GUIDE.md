# WeMatch API 使用指南

## 正确的API端点

### ❌ 错误的端点（您之前使用的）
```
http://localhost:8000/api/v1/properties/card_{card_id}
```
**错误原因**: 不存在 `/api/v1/properties` 路由

### ✅ 正确的端点

#### 1. 获取房源卡片
**端点**: `GET /api/v1/match/cards`

**参数**:
- `matchType`: 匹配类型 (`housing` 表示房源)
- `userRole`: 用户角色 (`seeker` 表示租客, `provider` 表示房东)
- `page`: 页码 (从1开始)
- `pageSize`: 每页数量 (1-50)

**示例**:
```
GET http://localhost:8000/api/v1/match/cards?matchType=housing&userRole=seeker&page=1&pageSize=5
```

#### 2. 获取用户资料
**端点**: `GET /api/v1/user/profile`

**参数**:
- `userId`: 用户ID

**示例**:
```
GET http://localhost:8000/api/v1/user/profile?userId=user_001
```

#### 3. 获取匹配详情
**端点**: `GET /api/v1/match/detail/{matchId}`

**示例**:
```
GET http://localhost:8000/api/v1/match/detail/match_123
```

#### 4. 创建匹配
**端点**: `POST /api/v1/match/action`

**请求体**:
```json
{
  "cardId": "card_xxx",
  "action": "like",
  "matchType": "housing"
}
```

## 测试数据

### 有效的测试用户ID
- user_001
- user_002  
- user_003
- user_004
- user_005

### 测试流程

1. **获取房源卡片**:
   ```bash
   curl "http://localhost:8000/api/v1/match/cards?matchType=housing&userRole=seeker&page=1&pageSize=5"
   ```

2. **获取房东信息**:
   ```bash
   curl "http://localhost:8000/api/v1/user/profile?userId=user_001"
   ```

3. **创建匹配**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/match/action" \
     -H "Content-Type: application/json" \
     -d '{"cardId":"card_xxx","action":"like","matchType":"housing"}'
   ```

## 快速测试

运行测试脚本:
```bash
# 生成测试数据
python app/utils/generate_valid_test_data.py

# 启动服务
python run.py

# 然后访问正确的端点
```

## 响应格式

所有API都返回统一格式:
```json
{
  "code": 0,
  "message": "success",
  "data": {...}
}
```

**注意**: `code=1404` 表示API不存在，请检查URL是否正确。