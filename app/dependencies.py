from fastapi import HTTPException, Depends, Header
from typing import Optional
from app.services.auth import AuthService
from app.utils.auth import get_current_user

# 创建AuthService的单例实例
auth_service = AuthService()

# 提供AuthService的依赖项
def get_auth_service():
    return auth_service

# 提供当前用户的依赖项
