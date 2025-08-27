from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any, Optional
from app.services.auth import auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(request: Request) -> Dict[str, Any]:
    """获取当前用户信息"""
    # 测试模式：允许无令牌直接使用默认测试用户
    if request.headers.get("X-Test-Mode", "").lower() == "true":
        user = auth_service.get_user_from_token("test_token_001")
        if user:
            return user

    # 正常模式：需要 Bearer token
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_header.split(" ", 1)[1]
    user = auth_service.get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_auth_service():
    """获取认证服务"""
    return auth_service
