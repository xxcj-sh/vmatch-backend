from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from app.models.schemas import FileUploadResponse, BaseResponse
from app.services.auth import auth_service
from app.services.mock_data import mock_data_service
from typing import Dict, Any, Optional
from app.config import settings
import os
import uuid

router = APIRouter()

@router.post("/upload", response_model=BaseResponse)
async def upload_file(
    file: UploadFile = File(...),
    type: str = Form(...),
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """上传文件接口"""
    # 验证文件类型
    if not file.content_type.startswith("image/"):
        return BaseResponse(
            code=400,
            message="请上传图片文件",
            data=None
        )
    
    # 验证文件大小
    # 在实际应用中，应该检查文件大小是否超过限制
    
    # 在测试模式下，模拟文件上传
    if settings.test_mode:
        result = mock_data_service.upload_file(type)
        return BaseResponse(
            code=0,
            message="success",
            data=FileUploadResponse(**result)
        )
    
    # 在生产环境中，保存文件
    try:
        # 确保上传目录存在
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # 生成唯一文件名
        file_ext = os.path.splitext(file.filename)[1]
        file_name = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(settings.upload_dir, file_name)
        
        # 保存文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 返回文件URL
        file_url = f"/uploads/{file_name}"
        return BaseResponse(
            code=0,
            message="success",
            data=FileUploadResponse(url=file_url)
        )
    except Exception as e:
        return BaseResponse(
            code=500,
            message=f"文件上传失败: {str(e)}",
            data=None
        )