# VMatch Backend

VMatch是一个基于FastAPI的后端服务，为微信小程序提供匹配功能。

## 功能特点

- 用户管理：注册、查询、更新和删除用户
- 匹配管理：创建、查询、更新和删除匹配记录
- 数据库支持：支持SQLite（开发环境）和云数据库（生产环境）

## 环境要求

- Python 3.7+
- FastAPI
- SQLAlchemy
- 数据库（SQLite/PostgreSQL/MySQL）

## 安装

1. 克隆仓库
```bash
git clone <repository-url>
cd vmatch-backend
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，设置环境变量
```

## 运行

```bash
uvicorn app.main:app --reload
```

访问 http://localhost:8000/docs 查看API文档。

## 数据库迁移

当前版本使用SQLite作为默认数据库，无需额外配置。如需使用其他数据库：

1. 在requirements.txt中取消注释相应的数据库驱动
2. 在.env文件中配置DATABASE_URL
3. 重新启动应用

## 云服务部署

本项目设计支持云服务部署，只需配置相应的环境变量：

1. 设置ENVIRONMENT=production
2. 配置DATABASE_URL为云数据库连接字符串
3. 设置其他必要的环境变量（如SECRET_KEY）

## API文档

启动服务后，访问以下URL查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc