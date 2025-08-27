from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.dependencies import get_current_user
from app.services.data_adapter import data_service

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
    responses={404: {"description": "Not found"}},
)

@router.get("/me")
def get_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """获取当前用户的资料"""
    return current_user

@router.put("/me")
def update_profile(profile_data: Dict[str, Any], current_user: Dict[str, Any] = Depends(get_current_user)):
    """更新用户资料"""
    user_id = current_user["id"]
    updated_user = data_service.update_profile(user_id, profile_data)
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user
