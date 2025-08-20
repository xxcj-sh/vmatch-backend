from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, user, match, chat, profile, file, membership
from app.config import settings
from app.utils.test_middleware import register_test_middleware

app = FastAPI(
    title="WeMatch 微信小程序服务端",
    description="基于 FastAPI 的微信小程序后端服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该配置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册测试中间件
register_test_middleware(app)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(user.router, prefix="/api/v1/user", tags=["用户"])
app.include_router(match.router, prefix="/api/v1/match", tags=["匹配"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["聊天"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["个人资料"])
app.include_router(file.router, prefix="/api/v1", tags=["文件上传"])
app.include_router(membership.router, prefix="/api/v1/membership", tags=["会员"])

@app.get("/")
async def root():
    return {"message": "WeMatch 微信小程序服务端运行正常"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)