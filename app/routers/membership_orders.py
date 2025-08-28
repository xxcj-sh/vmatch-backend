from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.order import MembershipOrder, OrderStatus
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/memberships", tags=["membership_orders"])

@router.get("/orders", summary="查询会员订单列表")
async def get_membership_orders(
    user_id: str = Query(..., description="用户ID"),
    status: Optional[str] = Query(None, description="订单状态: pending, paid, cancelled, refunded"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    查询用户的会员订单列表
    
    - **user_id**: 用户ID（必填）
    - **status**: 订单状态过滤（可选）
    - **page**: 页码，从1开始
    - **page_size**: 每页数量，最大100
    """
    try:
        # 构建查询
        query = db.query(MembershipOrder).filter(MembershipOrder.user_id == user_id)
        
        # 状态过滤
        if status:
            try:
                status_enum = OrderStatus(status)
                query = query.filter(MembershipOrder.status == status_enum)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"无效的订单状态: {status}")
        
        # 按创建时间倒序排列
        query = query.order_by(MembershipOrder.created_at.desc())
        
        # 分页
        offset = (page - 1) * page_size
        orders = query.offset(offset).limit(page_size).all()
        
        # 获取总数
        total = query.count()
        
        return {
            "code": 200,
            "message": "查询成功",
            "data": {
                "orders": [order.to_dict() for order in orders],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "total_pages": (total + page_size - 1) // page_size
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询订单失败: {str(e)}")

@router.get("/orders/{order_id}", summary="查询单个会员订单")
async def get_membership_order(
    order_id: str,
    user_id: str = Query(..., description="用户ID"),
    db: Session = Depends(get_db)
):
    """
    根据订单ID查询单个会员订单详情
    
    - **order_id**: 订单ID
    - **user_id**: 用户ID（用于权限验证）
    """
    try:
        order = db.query(MembershipOrder).filter(
            MembershipOrder.id == order_id,
            MembershipOrder.user_id == user_id
        ).first()
        
        if not order:
            raise HTTPException(status_code=404, detail="订单不存在")
        
        return {
            "code": 200,
            "message": "查询成功",
            "data": order.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询订单失败: {str(e)}")