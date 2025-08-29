# 用户角色资料API文档

## 概述

用户角色资料系统允许同一用户在不同场景下拥有多个不同的角色资料。每个用户可以创建多个资料，用于不同的匹配场景（如找房、交友、活动等）。

## 数据库设计

### 用户角色资料表 (user_profiles)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | TEXT | 资料ID (主键) |
| user_id | TEXT | 用户ID (外键) |
| role_type | TEXT | 角色类型 |
| scene_type | TEXT | 场景类型 |
| display_name | TEXT | 显示名称 |
| avatar_url | TEXT | 头像URL |
| bio | TEXT | 个人简介 |
| profile_data | TEXT | 角色特定数据 (JSON) |
| preferences | TEXT | 偏好设置 (JSON) |
| tags | TEXT | 标签列表 (JSON) |
| is_active | INTEGER | 是否激活 (1-激活, 0-停用) |
| visibility | TEXT | 可见性 (public/private/friends) |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

## 支持的场景和角色

### 1. 找房场景 (housing)
- **housing_seeker**: 找房者
- **housing_provider**: 房源提供者

### 2. 交友场景 (dating)
- **dating_seeker**: 交友者

### 3. 活动场景 (activity)
- **activity_organizer**: 活动组织者
- **activity_participant**: 活动参与者

## API接口

### 1. 获取用户所有角色资料

**GET** `/users/me/profiles`

**响应示例:**
```json
{
  "user_id": "test_user_001",
  "total_count": 5,
  "active_count": 5,
  "by_scene": [
    {
      "scene_type": "housing",
      "profiles": [
        {
          "id": "profile_housing_seeker_001",
          "user_id": "test_user_001",
          "role_type": "housing_seeker",
          "scene_type": "housing",
          "display_name": "小李找房",
          "avatar_url": "https://example.com/avatars/housing_seeker.jpg",
          "bio": "刚毕业的程序员，寻找合适的合租房源",
          "profile_data": {...},
          "preferences": {...},
          "tags": ["程序员", "安静", "整洁"],
          "is_active": 1,
          "visibility": "public",
          "created_at": "2025-01-29T01:00:00",
          "updated_at": "2025-01-29T01:00:00"
        }
      ]
    }
  ],
  "all_profiles": [...]
}
```

### 2. 获取特定场景下的角色资料

**GET** `/users/me/profiles/{scene_type}`

**路径参数:**
- `scene_type`: 场景类型 (housing/dating/activity)

**响应示例:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "scene_type": "housing",
    "profiles": [
      {
        "id": "profile_housing_seeker_001",
        "role_type": "housing_seeker",
        "display_name": "小李找房",
        ...
      }
    ]
  }
}
```

### 3. 获取特定角色的资料

**GET** `/users/me/profiles/{scene_type}/{role_type}`

**路径参数:**
- `scene_type`: 场景类型
- `role_type`: 角色类型

**响应示例:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "profile_housing_seeker_001",
    "user_id": "test_user_001",
    "role_type": "housing_seeker",
    "scene_type": "housing",
    "display_name": "小李找房",
    "profile_data": {
      "budget_range": [2000, 3500],
      "preferred_areas": ["朝阳区", "海淀区"],
      "room_type": "single_room",
      "occupation": "软件工程师"
    },
    "preferences": {
      "roommate_gender": "any",
      "shared_facilities": ["kitchen", "living_room"]
    },
    "tags": ["程序员", "安静", "整洁"]
  }
}
```

### 4. 创建用户角色资料

**POST** `/users/me/profiles`

**请求体:**
```json
{
  "role_type": "housing_seeker",
  "scene_type": "housing",
  "display_name": "小李找房",
  "avatar_url": "https://example.com/avatar.jpg",
  "bio": "寻找合适的合租房源",
  "profile_data": {
    "budget_range": [2000, 3500],
    "preferred_areas": ["朝阳区"]
  },
  "preferences": {
    "roommate_gender": "any"
  },
  "tags": ["程序员", "安静"],
  "visibility": "public"
}
```

### 5. 更新用户角色资料

**PUT** `/users/me/profiles/{profile_id}`

**请求体:** (所有字段都是可选的)
```json
{
  "display_name": "更新后的名称",
  "bio": "更新后的简介",
  "profile_data": {...},
  "preferences": {...},
  "tags": [...],
  "visibility": "private"
}
```

### 6. 删除用户角色资料

**DELETE** `/users/me/profiles/{profile_id}`

### 7. 切换资料激活状态

**PATCH** `/users/me/profiles/{profile_id}/toggle?is_active=1`

**查询参数:**
- `is_active`: 激活状态 (1-激活, 0-停用)

## 测试数据

系统已为用户 `test_user_001` 创建了以下测试资料：

1. **找房者资料** (housing_seeker)
   - 显示名称: 小李找房
   - 预算: 2000-3500元
   - 偏好区域: 朝阳区、海淀区、昌平区

2. **房东资料** (housing_provider)
   - 显示名称: 李房东
   - 房源: 望京SOHO 2室1厅
   - 租金: 3200元

3. **交友资料** (dating_seeker)
   - 显示名称: 阳光小李
   - 年龄: 26岁
   - 兴趣: 摄影、旅行、美食

4. **活动组织者资料** (activity_organizer)
   - 显示名称: 活动达人小李
   - 专长: 户外徒步、摄影聚会、美食探店

5. **活动参与者资料** (activity_participant)
   - 显示名称: 爱玩小李
   - 兴趣: 摄影、徒步、美食、电影

## 使用场景

1. **多角色切换**: 用户可以在不同场景下展示不同的身份
2. **精准匹配**: 根据不同角色的特定需求进行匹配
3. **隐私保护**: 不同角色可以设置不同的可见性
4. **个性化展示**: 每个角色都有独立的头像、简介和标签

## 注意事项

1. 每个用户在同一场景和角色组合下只能有一个资料
2. 资料的 `profile_data` 和 `preferences` 字段根据不同角色类型有不同的结构
3. 所有API都需要用户认证
4. 删除用户时会级联删除所有相关的角色资料