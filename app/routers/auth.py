from fastapi import APIRouter, Depends, HTTPException, Request, Form
from app.models.schemas import (
    BaseResponse, 
    LoginRequest, 
    LoginResponse,
    UserInfo
)
from app.services.auth import auth_service
from app.utils.auth import get_current_user
from app.dependencies import get_auth_service
from pydantic import ValidationError

router = APIRouter()

@router.post("/sessions", response_model=BaseResponse)
async def login(
    request: Request,
    auth_service = Depends(get_auth_service)
):
    try:
        # Parse the request body manually to catch validation errors
        body = await request.json()
        
        # Check if code is provided in the request
        if "code" not in body:
            return BaseResponse(code=422, message="缺少code参数")
        
        # Check if code is empty
        if not body["code"] or not isinstance(body["code"], str) or not body["code"].strip():
            return BaseResponse(code=422, message="code不能为空")
        
        # Create user_info if provided
        user_info = None
        if "userInfo" in body and isinstance(body["userInfo"], dict):
            try:
                user_info = UserInfo(
                    nick_name=body["userInfo"].get("nickName"),
                    avatar_url=body["userInfo"].get("avatarUrl"),
                    gender=body["userInfo"].get("gender")
                )
            except:
                pass
        
        # 验证登录请求
        login_result = auth_service.login(
            code=body["code"],
            user_info=user_info
        )
        
        # 构建响应数据
        return BaseResponse(
            code=0,
            message="success",
            data={
                "token": login_result["token"],
                "expiresIn": login_result["expiresIn"],
                "userInfo": login_result["userInfo"]
            }
        )
    except ValidationError as e:
        # Handle validation errors specifically
        return BaseResponse(code=422, message="验证错误")
    except ValueError as e:
        # Handle value errors
        return BaseResponse(code=422, message=str(e))
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug print
        return BaseResponse(code=1001, message=str(e))

@router.post("/sessions/phone", response_model=BaseResponse)
async def login_by_phone(
    request: Request,
    auth_service = Depends(get_auth_service)
):
    try:
        body = await request.json()
        phone = body.get("phone")
        code = body.get("code")
        
        if not phone or not code:
            return BaseResponse(code=422, message="缺少必要参数")
        
        login_result = auth_service.login_by_phone(phone, code)
        
        return BaseResponse(
            code=0,
            message="success",
            data={
                "token": login_result["token"],
                "expiresIn": login_result["expiresIn"],
                "userInfo": login_result["userInfo"]
            }
        )
    except Exception as e:
        return BaseResponse(code=1002, message=str(e))

@router.post("/sms-codes", response_model=BaseResponse)
async def send_sms_code(
    request: Request
):
    try:
        body = await request.json()
        phone = body.get("phone")
        
        if not phone:
            return BaseResponse(code=422, message="缺少手机号")
        
        # In test mode, just return success
        return BaseResponse(
            code=0,
            message="success",
            data={"sent": True}
        )
    except Exception as e:
        return BaseResponse(code=1003, message=str(e))

@router.get("/validate", response_model=BaseResponse)
async def validate_token(
    current_user: dict = Depends(get_current_user)
):
    # 令牌验证通过，返回用户信息
    return BaseResponse(
        code=0,
        message="success",
        data={"valid": True, "user_info": current_user}
    )

@router.get("/sessions/current", response_model=BaseResponse)
async def get_current_session(
    current_user: dict = Depends(get_current_user)
):
    # 获取当前会话信息
    return BaseResponse(
        code=0,
        message="success",
        data={
            "valid": True,
            "user": {
                "id": current_user.get("id"),
                "nickName": current_user.get("nickName")
            }
        }
    )

@router.delete("/sessions/current", response_model=BaseResponse)
async def logout():
    # 登出操作
    return BaseResponse(
        code=0,
        message="Logged out successfully"
    )
