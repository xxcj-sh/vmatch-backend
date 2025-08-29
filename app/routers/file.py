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
    if not file.content_type or not file.content_type.startswith("image/"):
        return BaseResponse(
            code=400,
            message="请上传图片文件",
            data=None
        )
    
    # 验证文件大小
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    # 检查文件大小是否超过限制 (默认10MB)
    max_file_size = getattr(settings, 'MAX_FILE_SIZE', 10 * 1024 * 1024)
    if file_size > max_file_size:
        return BaseResponse(
            code=400,
            message=f"文件大小超过限制，最大允许 {max_file_size // (1024 * 1024)}MB",
            data=None
        )
    
    # 重置文件指针，因为我们已经读取了文件内容
    await file.seek(0)
    
    # 保存文件到本地
    try:
        # 确保上传目录存在
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # 生成唯一文件名
        filename = file.filename or "unknown"
        file_ext = os.path.splitext(filename)[1]
        file_name = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, file_name)
        
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

@router.delete("/delete", response_model=BaseResponse)
async def delete_file(
    file_url: str = Form(...),
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
):
    """删除文件接口"""
    try:
        # 在开发环境下，模拟文件删除
        if settings.ENVIRONMENT == "development":
            return BaseResponse(
                code=0,
                message="文件删除成功",
                data=None
            )
        
        # 从URL中提取文件名
        if file_url.startswith("/uploads/"):
            file_name = file_url.replace("/uploads/", "")
            file_path = os.path.join(settings.UPLOAD_DIR, file_name)
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return BaseResponse(
                    code=404,
                    message="文件不存在",
                    data=None
                )
            
            # 删除文件
            os.remove(file_path)
            return BaseResponse(
                code=0,
                message="文件删除成功",
                data=None
            )
        else:
            return BaseResponse(
                code=400,
                message="无效的文件URL",
                data=None
            )
            
    except Exception as e:
        return BaseResponse(
            code=500,
            message=f"文件删除失败: {str(e)}",
            data=None
        )
