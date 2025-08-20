# WeMatch微信小程序服务端接口文档

## 基础信息

### 接口前缀
所有接口前缀为 `/api/v1`

### 请求/响应格式
- 请求格式：JSON
- 响应格式：统一使用 BaseResponse 格式，包含以下字段：
  - `code`: 状态码，0 表示成功，非 0 表示失败
  - `message`: 响应消息
  - `data`: 响应数据（可选）

### 公共响应参数
所有接口返回格式统一如下：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    // 具体接口数据
  }
}
```

### 错误码
| 错误码 | 描述 |
| --- | --- |
| 0 | 成功 |
| 1001 | 登录失败 |
| 1002 | 手机登录失败 |
| 1003 | 发送验证码失败 |
| 1004 | 注册失败 |
| 1005 | 注销失败 |
| 2001 | 获取用户信息失败 |
| 2002 | 更新用户信息失败 |
| 3001 | 获取匹配卡片失败 |
| 3002 | 匹配操作失败 |
| 3003 | 获取匹配列表失败 |
| 4001 | 获取聊天历史失败 |
| 4002 | 发送消息失败 |
| 4003 | 标记消息已读失败 |
| 5001 | 文件上传失败 |
| 9999 | 系统错误 |

## 用户认证接口

### 1. 登录接口
- 路径: `/api/v1/auth/login`
- 方法: POST
- 请求参数:
  ```json
  {
    "code": "string", // 登录凭证code
    "user_info": {
      "nick_name": "string", // 昵称
      "avatar_url": "string", // 头像URL
      "gender": 0 // 性别
    }
  }
  ```
- 响应数据:
  ```json
  {
    "token": "string", // 用户token
    "expires_in": 3600, // token过期时间(秒)
    "user_info": {
      // 用户信息
    }
  }
  ```

### 2. 手机登录接口
- 路径: `/api/v1/auth/login/phone`
- 方法: POST
- 请求参数:
  ```json
  {
    "phone": "string", // 手机号
    "sms_code": "string" // 验证码
  }
  ```
- 响应数据:
  ```json
  {
    "token": "string", // 用户token
    "expires_in": 3600, // token过期时间(秒)
    "user_info": {
      // 用户信息
    }
  }
  ```

### 3. 发送验证码接口
- 路径: `/api/v1/auth/sms-code`
- 方法: POST
- 请求参数:
  ```json
  {
    "phone": "string" // 手机号
  }
  ```
- 响应数据: 无

### 4. 注册接口
- 路径: `/api/v1/auth/register`
- 方法: POST
- 请求参数:
  ```json
  {
    "user_info": {
      "nick_name": "string", // 昵称
      "avatar_url": "string", // 头像URL
      "gender": 0 // 性别
    }
  }
  ```
- 响应数据: 无

### 5. 注销接口
- 路径: `/api/v1/auth/logout`
- 方法: POST
- 请求参数: 无 (需要登录态)
- 响应数据: 无

### 6. 验证令牌接口
- 路径: `/api/v1/auth/validate`
- 方法: GET
- 请求参数: 无 (需要登录态)
- 响应数据:
  ```json
  {
    "user_info": {
      // 用户信息
    }
  }
  ```

## 用户信息接口
(继续更新其他接口...)