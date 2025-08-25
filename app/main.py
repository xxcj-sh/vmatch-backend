from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, user, profile, match, chat, file, membership, properties, scenes
from app.config import settings
from app.utils.restful_test_middleware import register_restful_test_middleware

app = FastAPI(
    title="WeMatch 微信小程序服务端",
    description="基于 FastAPI 的微信小程序后端服务 - RESTful API",
    version="2.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该配置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 RESTful 测试中间件
register_restful_test_middleware(app)

# RESTful 路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(profile.router, prefix="/api/v1/profiles", tags=["Profiles"])
app.include_router(match.router, prefix="/api/v1/matches", tags=["Matches"])
app.include_router(chat.router, prefix="/api/v1/messages", tags=["Messages"])
app.include_router(file.router, prefix="/api/v1/files", tags=["Files"])
app.include_router(membership.router, prefix="/api/v1/memberships", tags=["Memberships"])
app.include_router(properties.router, prefix="/api/v1/properties", tags=["Properties"])
app.include_router(scenes.router, prefix="/api/v1/scenes", tags=["Scenes"])
# Add scenarios alias for backward compatibility
app.include_router(scenes.router, prefix="/api/v1/scenarios", tags=["Scenarios"])

@app.get("/")
async def root():
    return {
        "message": "WeMatch 微信小程序服务端运行正常",
        "version": "2.0.0",
        "api_design": "RESTful"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0"
    }

@app.get("/api/v1")
async def api_info():
    return {
        "version": "2.0.0",
        "design": "RESTful",
        "test_mode_header": "X-Test-Mode: true",
        "endpoints": {
            "auth": "/api/v1/auth",
            "users": "/api/v1/users",
            "profiles": "/api/v1/profiles",
            "matches": "/api/v1/matches",
            "messages": "/api/v1/messages",
            "files": "/api/v1/files",
            "memberships": "/api/v1/memberships",
            "properties": "/api/v1/properties",
            "scenes": "/api/v1/scenes"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
