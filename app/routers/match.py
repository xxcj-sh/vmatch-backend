from fastapi import APIRouter, Depends, Query, Path, Request
from app.models.schemas import (
    MatchCardsResponse, MatchActionRequest, MatchActionResponse, 
    MatchListResponse, BaseResponse
)
from app.services.auth import auth_service
from app.services.mock_data import mock_data_service
from typing import Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter()

class SwipeRequest(BaseModel):
    cardId: str
    direction: str  # left/right/up

@router.get("/cards", response_model=BaseResponse)
async def get_match_cards(
    matchType: Optional[str] = Query(None, description="匹配类型(housing/activity/dating)"),
    userRole: Optional[str] = Query(None, description="用户角色(seeker/provider)"),
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=50, description="每页数量"),
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """获取匹配卡片"""
    # Check required parameters
    if not matchType or not userRole:
        return BaseResponse(
            code=422,
            message="缺少必要参数",
            data=None
        )
    
    result = mock_data_service.get_cards(matchType, userRole, page, pageSize)
    return BaseResponse(
        code=0,
        message="success",
        data=result
    )

@router.post("/action", response_model=BaseResponse)
async def submit_match_action(
    request: Request,
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """提交匹配操作"""
    try:
        # Parse request body
        body = await request.json()
        
        # Check required fields
        if not body.get("cardId") or not body.get("action") or not body.get("matchType"):
            return BaseResponse(
                code=422,
                message="缺少必要参数",
                data=None
            )
        
        result = mock_data_service.create_match(current_user["id"], body.get("cardId"), body.get("action"))
        return BaseResponse(
            code=0,
            message="success",
            data=MatchActionResponse(**result)
        )
    except Exception as e:
        return BaseResponse(
            code=500,
            message=f"操作失败: {str(e)}",
            data=None
        )

@router.post("/swipe", response_model=BaseResponse)
async def swipe_card(
    request: SwipeRequest,
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """滑动卡片操作"""
    # 将滑动方向转换为操作类型
    action = "like" if request.direction == "right" else "superlike" if request.direction == "up" else "dislike"
    result = mock_data_service.create_match(current_user["id"], request.cardId, action)
    return BaseResponse(
        code=0,
        message="success",
        data={"isMatch": result["isMatch"]}
    )

@router.get("/detail/{matchId}", response_model=BaseResponse)
async def get_match_detail(
    matchId: str = Path(..., description="匹配ID"),
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """获取匹配详情"""
    match = mock_data_service.matches.get(matchId)
    if not match:
        return BaseResponse(
            code=1002,
            message="匹配不存在",
            data=None
        )
    
    # 检查用户是否有权限查看该匹配
    if match["userId1"] != current_user["id"] and match["userId2"] != current_user["id"]:
        return BaseResponse(
            code=403,
            message="权限不足",
            data=None
        )
    
    # 获取匹配的另一方用户ID
    other_user_id = match["userId2"] if match["userId1"] == current_user["id"] else match["userId1"]
    other_user = mock_data_service.get_user_by_id(other_user_id)
    
    if not other_user:
        # 如果是卡片，获取卡片信息
        card = next((card for card in mock_data_service.cards if card["id"] == match["cardId"]), None)
        if card:
            detail_data = {
                "id": match["id"],
                "name": card.get("name", ""),
                "avatar": card.get("avatar", ""),
                "age": card.get("age"),
                "location": card.get("location", ""),
                "occupation": card.get("occupation", ""),
                "education": card.get("education", ""),
                "height": card.get("height"),
                "reason": match.get("reason", "")
            }
        else:
            return BaseResponse(
                code=1002,
                message="匹配详情不存在",
                data=None
            )
    else:
        # 如果是用户，获取用户信息
        detail_data = {
            "id": match["id"],
            "name": other_user.get("nickName", ""),
            "avatar": other_user.get("avatarUrl", ""),
            "age": other_user.get("age"),
            "location": other_user.get("location", ""),
            "occupation": other_user.get("occupation", ""),
            "education": other_user.get("education", ""),
            "height": other_user.get("height"),
            "reason": match.get("reason", "")
        }
    
    return BaseResponse(
        code=0,
        message="success",
        data=detail_data
    )

@router.get("/list", response_model=BaseResponse)
async def get_match_list(
    status: str = Query("all", description="状态(all/new/contacted)"),
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=50, description="每页数量"),
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """获取匹配列表"""
    result = mock_data_service.get_matches(current_user["id"], status, page, pageSize)
    return BaseResponse(
        code=0,
        message="success",
        data=result
    )