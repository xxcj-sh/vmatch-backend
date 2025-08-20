from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth import auth_service
from typing import Dict, Any

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """获取当前登录用户"""
    token = credentials.credentials
    user = auth_service.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="无效的token")
    return user