from fastapi import APIRouter, Depends
from app.models.schemas import BaseResponse
from app.services.auth import auth_service
from typing import Dict, Any
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/memberships", tags=["memberships"])

class PaymentRequest(BaseModel):
    planId: str

@router.get("/me", response_model=BaseResponse)
async def get_membership_info(current_user: Dict[str, Any] = Depends(auth_service.get_current_user)):
    """获取会员信息"""
    # 在测试模式下，返回模拟的会员信息
    membership_data = {
        "level": "free",
        "levelName": "免费会员",
        "expireDate": None,
        "features": ["基础匹配", "每日10次滑动"],
        "remainingSwipes": 10,
        "totalSwipes": 10
    }
    
    return BaseResponse(
        code=0,
        message="success",
        data=membership_data
    )

@router.post("/orders", response_model=BaseResponse)
async def create_membership_payment(
    request: PaymentRequest,
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """创建会员支付"""
    # 在测试模式下，返回模拟的支付信息
    payment_data = {
        "orderId": f"order_{uuid.uuid4()}",
        "amount": 30.00,
        "status": "pending",
        "paymentUrl": "https://example.com/payment"
    }
    
    return BaseResponse(
        code=0,
        message="success",
        data=payment_data
    )