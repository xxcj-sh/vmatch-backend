# 前后端联调配置说明

## 当前配置状态

✅ **已完成的配置调整：**

1. **关闭测试模式**
   - 设置 `TEST_MODE=false` 在 `.env` 文件中
   - 移除了测试相关的工具文件和脚本

2. **开启前后端联调模式**
   - 添加了 CORS 中间件支持跨域请求
   - 服务器运行在 `http://0.0.0.0:8000`
   - 支持热重载，便于开发调试

3. **数据库配置**
   - 使用开发数据库 `vmatch_dev.db`
   - 支持真实的数据查询和访问

## API 服务地址

- **本地开发服务器**: `http://localhost:8000`
- **API 文档**: `http://localhost:8000/docs`
- **API 根路径**: `/api/v1`

## 主要 API 端点

- 用户认证: `/api/v1/auth/`
- 用户管理: `/api/v1/users/`
- 匹配服务: `/api/v1/matches/`
- 文件上传: `/api/v1/upload`

## 前端集成注意事项

1. **跨域配置**: 已启用 CORS，允许所有来源访问
2. **认证方式**: 使用 token 认证，需在请求头中添加 `Authorization: Bearer <token>`
3. **开发环境**: 当前为开发模式，使用模拟的微信登录和简化的 token 处理

## 启动服务

```bash
python run.py
```

服务器将在 `http://0.0.0.0:8000` 启动，支持热重载。

## 环境变量配置

当前 `.env` 配置：
```
ENVIRONMENT=development
TEST_MODE=false
DATABASE_URL=sqlite:///./vmatch_dev.db
SECRET_KEY=vmatch_development_secret_key_2025