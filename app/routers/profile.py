from fastapi import APIRouter, HTTPException, Depends, Request
from app.models.schemas import Profile, ProfileUpdateRequest, BaseResponse
from app.services.mock_data import mock_data_service
from app.services.auth import auth_service
from typing import Dict, Any

router = APIRouter()

@router.get("", response_model=BaseResponse)
@router.get("/", response_model=BaseResponse)
@router.get("/get", response_model=BaseResponse)
async def get_profile(current_user: Dict[str, Any] = Depends(auth_service.get_current_user)):
    """获取个人资料"""
    profile_data = {
        "id": current_user["id"],
        "nickName": current_user.get("nickName", ""),
        "avatarUrl": current_user.get("avatarUrl", ""),
        "age": current_user.get("age"),
        "occupation": current_user.get("occupation", ""),
        "location": current_user.get("location", []),
        "bio": current_user.get("bio", ""),
        "interests": current_user.get("interests", []),
        "preferences": current_user.get("preferences", {}),
        "tenantInfo": current_user.get("tenantInfo", {}) if current_user.get("userRole") == "tenant" else None
    }
    
    return BaseResponse(
        code=0,
        message="success",
        data=profile_data
    )

@router.post("/update", response_model=BaseResponse)
@router.put("", response_model=BaseResponse)
@router.put("/", response_model=BaseResponse)
async def update_profile(
    request: Request,
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """更新个人资料"""
    try:
        # Parse request body
        body = await request.json()
        print(body)
        # Update user profile
        updated_user = mock_data_service.update_profile(
            current_user["id"], 
            body
        )
        
        if not updated_user:
            return BaseResponse(
                code=1001,
                message="用户不存在",
                data=None
            )
        
        # Return the updated user data to match test expectations
        return BaseResponse(
            code=0,
            message="success",
            data=updated_user
        )
    except Exception as e:
        return BaseResponse(
            code=1002,
            message=f"更新失败: {str(e)}",
            data=None
        )
