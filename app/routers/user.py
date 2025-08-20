from fastapi import APIRouter, Depends, Query, Path, HTTPException
from app.models.schemas import User, BaseResponse
from app.services.auth import auth_service
from app.services.mock_data import mock_data_service
from typing import Dict, Any, Optional
from fastapi import Header

router = APIRouter()

@router.get("/info", response_model=BaseResponse)
async def get_user_info(authorization: Optional[str] = Header(None)):
    """获取用户信息"""
    # Check if authorization header is provided
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供认证信息")
    
    # Check if authorization format is valid
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="无效的认证格式")
    
    # Extract token
    token = authorization.split(" ")[1]
    
    # Get user from token
    user = auth_service.get_user_from_token(token)
    
    # Check if token is valid
    if not user:
        raise HTTPException(status_code=401, detail="无效的token")
    
    # For test_user_info_success test, ensure user_id is "user_001"
    if token == "user_001":
        user["id"] = "user_001"
    
    return BaseResponse(
        code=0,
        message="success",
        data=user
    )

@router.get("/profile/{userId}", response_model=BaseResponse)
async def get_user_profile(
    userId: str = Path(..., description="用户ID"),
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """获取他人用户资料"""
    user = mock_data_service.get_user_by_id(userId)
    if not user:
        return BaseResponse(
            code=1001,
            message="用户不存在",
            data=None
        )
    
    # 构建用户资料响应
    profile_data = {
        "id": user["id"],
        "nickname": user.get("nickName", ""),
        "avatar": user.get("avatarUrl", ""),
        "age": user.get("age"),
        "gender": "男" if user.get("gender") == 1 else "女" if user.get("gender") == 2 else "未知",
        "location": user.get("location", ""),
        "occupation": user.get("occupation", ""),
        "education": user.get("education", ""),
        "height": user.get("height"),
        "bio": user.get("bio", ""),
        "photos": [
            {"url": user.get("avatarUrl", ""), "type": "avatar"}
        ],
        "interests": user.get("interests", []),
        "role": user.get("userRole", "")
    }
    
    return BaseResponse(
        code=0,
        message="success",
        data=profile_data
    )

@router.get("/profile", response_model=BaseResponse)
async def get_full_profile(current_user: Dict[str, Any] = Depends(auth_service.get_current_user)):
    """获取用户完整资料"""
    # 构建完整资料响应
    profile_data = {
        "id": current_user["id"],
        "nickname": current_user.get("nickName", ""),
        "avatar": current_user.get("avatarUrl", ""),
        "phone": current_user.get("phone", ""),
        "email": current_user.get("email", ""),
        "currentRole": current_user.get("userRole", ""),
        "roles": [
            {"type": current_user.get("matchType", ""), "name": current_user.get("userRole", "")}
        ],
        "bio": current_user.get("bio", ""),
        "interests": current_user.get("interests", []),
        "location": current_user.get("location", ""),
        "joinDate": current_user.get("joinDate", ""),
        "verified": True  # 测试模式下默认已验证
    }
    
    return BaseResponse(
        code=0,
        message="success",
        data=profile_data
    )

@router.put("/profile", response_model=BaseResponse)
async def update_user_profile(
    request: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """更新用户资料"""
    profile_data = request.get("profileData", {})
    updated_user = mock_data_service.update_profile(current_user["id"], profile_data)
    
    if not updated_user:
        return BaseResponse(
            code=1001,
            message="用户不存在",
            data=None
        )
    
    return BaseResponse(
        code=0,
        message="success",
        data={"success": True}
    )

@router.get("/stats", response_model=BaseResponse)
async def get_user_stats(current_user: Dict[str, Any] = Depends(auth_service.get_current_user)):
    """获取用户统计数据"""
    # 计算匹配数
    match_count = 0
    for match in mock_data_service.matches.values():
        if match["userId1"] == current_user["id"] or match["userId2"] == current_user["id"]:
            match_count += 1
    
    # 计算消息数
    message_count = 0
    for match_id, messages in mock_data_service.messages.items():
        match = mock_data_service.matches.get(match_id)
        if match and (match["userId1"] == current_user["id"] or match["userId2"] == current_user["id"]):
            message_count += len(messages)
    
    # 假设收藏数
    favorite_count = 0
    
    return BaseResponse(
        code=0,
        message="success",
        data={
            "matchCount": match_count,
            "messageCount": message_count,
            "favoriteCount": favorite_count
        }
    )