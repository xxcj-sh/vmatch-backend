# WeMatch RESTful API

## 项目概述
WeMatch 微信小程序后端服务，采用 RESTful API 设计规范。

## 核心特性
- ✅ RESTful API 设计规范
- ✅ 统一的响应格式
- ✅ 简化的测试模式
- ✅ 完整的 API 文档
- ✅ 自动化测试覆盖

## 快速开始

### 启动服务
```bash
python app/main.py
```

### 测试模式
在任何 API 请求中添加头部启用测试模式：
```http
X-Test-Mode: true
```

### 运行测试
```bash
python -m pytest tests/test_restful_api.py -v
```

## API 端点

### 认证 (Authentication)
- `POST /api/v1/auth/sessions` - 登录
- `GET /api/v1/auth/sessions/current` - 验证会话
- `DELETE /api/v1/auth/sessions/current` - 登出

### 用户 (Users)
- `GET /api/v1/users/me` - 获取当前用户信息
- `PUT /api/v1/users/me` - 更新当前用户信息
- `GET /api/v1/users/{userId}` - 获取用户资料

### 个人资料 (Profiles)
- `GET /api/v1/profiles/me` - 获取个人资料
- `PUT /api/v1/profiles/me` - 更新个人资料

### 匹配 (Matches)
- `GET /api/v1/matches/cards` - 获取匹配卡片
- `POST /api/v1/matches/actions` - 提交匹配操作
- `GET /api/v1/matches` - 获取匹配列表

### 消息 (Messages)
- `GET /api/v1/messages` - 获取消息列表
- `POST /api/v1/messages` - 发送消息
- `PUT /api/v1/messages/read` - 标记已读

### 文件 (Files)
- `POST /api/v1/files` - 上传文件

### 会员 (Memberships)
- `GET /api/v1/memberships/me` - 获取会员信息
- `POST /api/v1/memberships/orders` - 创建会员订单

### 房源 (Properties)
- `GET /api/v1/properties/{propertyId}` - 获取房源详情

### 场景 (Scenes)
- `GET /api/v1/scenes` - 获取场景配置
- `GET /api/v1/scenes/{sceneKey}` - 获取指定场景

## 文档
- `docs/api_reference_complete.md` - 完整 API 参考文档
- `docs/api_reference_final.md` - 简洁版 API 参考

## 测试
- `tests/test_restful_api.py` - RESTful API 测试套件
- 26/32 测试通过，核心功能正常

## 项目结构
```
app/
├── main.py                           # 主应用入口
├── routers/                          # 路由模块
├── services/                         # 业务逻辑
├── utils/
│   └── restful_test_middleware.py    # RESTful 测试中间件
docs/                                 # API 文档
tests/
└── test_restful_api.py              # RESTful API 测试
```

## 开发指南

### 测试示例
```bash
# 登录
curl -X POST http://localhost:8000/api/v1/auth/sessions \
  -H "Content-Type: application/json" \
  -H "X-Test-Mode: true" \
  -d '{"code": "test_code"}'

# 获取用户信息
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "X-Test-Mode: true"

# 获取匹配卡片
curl -X GET "http://localhost:8000/api/v1/matches/cards?matchType=housing&userRole=seeker" \
  -H "X-Test-Mode: true"
```

### 客户端集成
参考 `docs/api_reference_complete.md` 中的 JavaScript 和微信小程序示例。

## 版本信息
- **版本**: 2.0.0
- **设计**: RESTful
- **测试模式**: 支持
- **文档**: 完整