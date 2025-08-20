from fastapi import APIRouter, Depends, Path, HTTPException
from app.models.schemas import BaseResponse
from app.services.auth import auth_service
from app.services.mock_data import mock_data_service
from typing import Dict, Any

router = APIRouter()

@router.get("/{card_id}", response_model=BaseResponse)
async def get_property_detail(
    card_id: str = Path(..., description="卡片ID"),
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """获取房源/卡片详情"""
    
    # 从mock数据中查找卡片
    card = mock_data_service.cards.get(card_id)
    if not card:
        # 检查用户卡片
        card = mock_data_service.users.get(card_id)
    
    if not card:
        return BaseResponse(
            code=1404,
            message=f"卡片 {card_id} 不存在",
            data=None
        )
    
    # 构建房源详情数据
    property_detail = {
        "id": card["id"],
        "type": card.get("type", ""),
        "title": card.get("title", ""),
        "description": card.get("description", ""),
        "price": card.get("price", 0),
        "location": card.get("location", ""),
        "area": card.get("area", 0),
        "rooms": card.get("rooms", 0),
        "floor": card.get("floor", ""),
        "orientation": card.get("orientation", ""),
        "decoration": card.get("decoration", ""),
        "images": card.get("images", []),
        "landlord": card.get("landlordInfo", {}),
        "facilities": card.get("facilities", []),
        "tags": card.get("tags", []),
        "publishTime": card.get("publishTime", ""),
        "contact": card.get("contact", {})
    }
    
    return BaseResponse(
        code=0,
        message="success",
        data=property_detail
    )