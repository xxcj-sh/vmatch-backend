# WeMatch 微信小程序服务端

基于 FastAPI 的微信小程序后端服务，提供用户认证、匹配、聊天、个人资料管理等完整功能。

## 项目特性

- ✅ 完整的 RESTful API 设计
- ✅ 微信登录集成
- ✅ 用户匹配系统
- ✅ 实时聊天功能
- ✅ 个人资料管理
- ✅ 文件上传功能
- ✅ 测试模式支持（无需数据库）
- ✅ 完整的测试用例
- ✅ 详细的API文档

## 技术栈

- **框架**: FastAPI (Python)
- **测试**: pytest + httpx
- **认证**: JWT (测试模式下简化)
- **数据**: 测试模式使用内存数据，生产模式支持数据库

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

#### 开发模式
```bash
python run.py
```

#### 使用uvicorn直接启动
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问API文档

启动后访问: http://localhost:8000/docs

## API接口

### 1. 认证接口
- `POST /api/v1/auth/login` - 微信登录

### 2. 用户接口
- `GET /api/v1/user/info` - 获取用户信息

### 3. 匹配接口
- `GET /api/v1/match/cards` - 获取匹配卡片
- `POST /api/v1/match/action` - 提交匹配操作
- `GET /api/v1/match/list` - 获取匹配列表

### 4. 聊天接口
- `GET /api/v1/chat/history` - 获取聊天记录
- `POST /api/v1/chat/send` - 发送消息
- `POST /api/v1/chat/read` - 标记消息已读

### 5. 个人资料接口
- `GET /api/v1/profile/get` - 获取个人资料
- `POST /api/v1/profile/update` - 更新个人资料

### 6. 文件上传接口
- `POST /api/v1/file/upload` - 上传图片

## 测试

### 运行所有测试
```bash
python run_tests.py
```

### 使用pytest运行测试
```bash
pytest -v tests/
```

### 运行特定测试
```bash
pytest tests/test_auth.py -v
pytest tests/test_match.py::TestMatch::test_get_match_cards_success -v
```

## 测试模式

本项目支持测试模式，即使没有数据库也能运行和测试：

- 测试模式使用内存中的模拟数据
- 所有接口都能返回测试数据
- 适合开发和测试阶段使用

在 `app/config.py` 中设置 `test_mode=True` 启用测试模式。

### 增强的测试环境

本项目新增了增强的测试环境功能，可以自动生成符合微信小程序API接口规范的测试数据：

#### 测试工具使用

项目提供了以下测试工具：

1. **测试中间件**：在测试模式下，会自动拦截API请求并返回模拟数据
2. **测试数据生成器**：提供各种API数据的生成方法
3. **测试工具类**：提供便捷的测试模式控制和测试数据生成功能

#### 示例代码

```python
# 导入测试工具
from app.utils.test_utils import test_utils

# 检查测试模式
is_test = test_utils.is_test_mode()

# 启用/禁用测试模式
test_utils.enable_test_mode()
test_utils.disable_test_mode()

# 生成测试数据
user = test_utils.generate_user_data()
card = test_utils.generate_card_data()
match = test_utils.generate_match_data()
message = test_utils.generate_message_data()

# 生成测试Token和请求头
token = test_utils.generate_test_token("user_001")
headers = test_utils.get_test_headers("user_001")

# 模拟API响应
from app.utils.test_data_generator import test_data_generator
response = test_data_generator.mock_api_response("/api/v1/user/info", "GET")
```

#### 运行测试示例

```bash
python -m app.utils.test_example
```

## 项目结构

```
vmatch-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # 主应用文件
│   ├── config.py            # 配置文件
│   ├── dependencies.py      # 依赖注入
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # 数据模型
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py          # 认证服务
│   │   └── mock_data.py     # 测试数据服务
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth.py          # 认证工具
│   │   ├── test_data_generator.py  # 测试数据生成器
│   │   ├── test_middleware.py      # 测试中间件
│   │   ├── test_utils.py           # 测试工具类
│   │   └── test_example.py         # 测试示例
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # 认证路由
│       ├── user.py          # 用户路由
│       ├── match.py         # 匹配路由
│       ├── chat.py          # 聊天路由
│       ├── profile.py       # 个人资料路由
│       └── file.py          # 文件上传路由
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # 测试配置
│   ├── test_auth.py         # 认证测试
│   ├── test_user.py         # 用户测试
│   ├── test_match.py        # 匹配测试
│   ├── test_chat.py         # 聊天测试
│   ├── test_profile.py      # 个人资料测试
│   ├── test_file.py         # 文件上传测试
│   └── test_integration.py  # 集成测试
├── requirements.txt         # 项目依赖
├── pytest.ini             # pytest配置
├── run.py                 # 启动脚本
├── run_tests.py          # 测试运行脚本
├── .env.example          # 环境变量示例
└── README.md             # 项目说明
```

## 环境配置

复制 `.env.example` 为 `.env` 并配置相关参数：

```bash
cp .env.example .env
```

## 生产环境部署

1. 设置 `test_mode=False`
2. 配置真实的数据库连接
3. 配置微信开发者凭证
4. 配置生产环境的安全密钥
5. 使用Docker或进程管理器部署

## 开发建议

1. **测试优先**: 所有功能都有对应的测试用例
2. **文档完整**: 使用FastAPI自动生成API文档
3. **类型安全**: 使用Pydantic进行数据验证
4. **错误处理**: 统一的错误响应格式
5. **日志记录**: 建议添加详细的日志记录

## 贡献指南

1. 添加新功能时同步更新测试用例
2. 保持代码风格一致
3. 更新API文档
4. 确保所有测试通过

## 许可证

MIT License