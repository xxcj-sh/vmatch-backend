from fastapi import APIRouter, Depends, Query, Path, Request, HTTPException, status
from app.models.schemas import (
    ChatHistoryResponse, SendMessageRequest, SendMessageResponse, 
    ReadMessageRequest, BaseResponse
)
from app.services.auth import auth_service
from app.services.mock_data import mock_data_service
from typing import Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter()

class ReadRequest(BaseModel):
    matchId: str

class SendMessageRequestModel(BaseModel):
    matchId: str
    content: str
    type: str

@router.get("/history", response_model=BaseResponse)
async def get_chat_history_query(
    matchId: Optional[str] = Query(None, description="匹配ID"),
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """通过查询参数获取聊天记录"""
    if not matchId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="缺少必要参数"
        )
    
    return await get_chat_history_internal(matchId, page, pageSize, current_user)

@router.get("/history/{matchId}", response_model=BaseResponse)
async def get_chat_history(
    matchId: str = Path(..., description="匹配ID"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """通过路径参数获取聊天记录"""
    return await get_chat_history_internal(matchId, page, limit, current_user)

async def get_chat_history_internal(
    matchId: str,
    page: int,
    limit: int,
    current_user: Dict[str, Any]
):
    """获取聊天记录内部实现"""
    # 检查匹配是否存在
    match = mock_data_service.matches.get(matchId)
    if not match:
        return BaseResponse(
            code=1002,
            message="匹配不存在",
            data=None
        )
    
    # 检查用户是否有权限查看该匹配的聊天记录
    if match["userId1"] != current_user["id"] and match["userId2"] != current_user["id"]:
        return BaseResponse(
            code=403,
            message="权限不足",
            data=None
        )
    
    result = mock_data_service.get_chat_history(matchId, page, limit)
    return BaseResponse(
        code=0,
        message="success",
        data=result
    )

@router.post("/send", response_model=BaseResponse)
async def send_message(
    request: SendMessageRequestModel,
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """发送消息"""
    try:
        # 检查匹配是否存在
        match = mock_data_service.matches.get(request.matchId)
        if not match:
            return BaseResponse(
                code=1002,
                message="匹配不存在",
                data=None
            )
        
        # 检查用户是否有权限发送消息
        if match["userId1"] != current_user["id"] and match["userId2"] != current_user["id"]:
            return BaseResponse(
                code=403,
                message="权限不足",
                data=None
            )
        
        result = mock_data_service.send_message(
            request.matchId, 
            current_user["id"], 
            request.content, 
            request.type
        )
        
        return BaseResponse(
            code=0,
            message="success",
            data=SendMessageResponse(
                id=result["id"],
                timestamp=result["timestamp"]
            )
        )
    except Exception as e:
        return BaseResponse(
            code=500,
            message=f"发送失败: {str(e)}",
            data=None
        )

@router.post("/read", response_model=BaseResponse)
async def mark_messages_read(
    request: ReadRequest,
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """标记消息已读"""
    # 检查匹配是否存在
    match = mock_data_service.matches.get(request.matchId)
    if not match:
        return BaseResponse(
            code=1002,
            message="匹配不存在",
            data=None
        )
    
    # 检查用户是否有权限标记消息已读
    if match["userId1"] != current_user["id"] and match["userId2"] != current_user["id"]:
        return BaseResponse(
            code=403,
            message="权限不足",
            data=None
        )
    
    # 标记消息已读
    # 在测试模式下，直接返回成功
    # 生产环境中需要更新数据库中的消息状态
    return BaseResponse(
        code=0,
        message="success",
        data={"success": True}
    )