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
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user_optional)
):
    """
    上传文件接口
    
    支持的文件类型：
    - 图片：JPEG, PNG, GIF, WebP (最大10MB)
    - 视频：MP4, AVI, MOV, WMV, FLV, WebM, MKV, 3GP (最大500MB)
    
    参数：
    - file: 要上传的文件
    - type: 文件类型标识（可选，用于业务逻辑分类）
    
    返回：
    - 成功：返回文件访问URL
    - 失败：返回错误信息
    """
    # 验证文件类型 - 支持图片和视频
    allowed_image_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
    allowed_video_types = ["video/mp4", "video/avi", "video/mov", "video/wmv", "video/flv", "video/webm", "video/mkv", "video/3gp"]
    
    if not file.content_type:
        return BaseResponse(
            code=400,
            message="无法识别文件类型",
            data=None
        )
    
    is_image = file.content_type in allowed_image_types
    is_video = file.content_type in allowed_video_types
    
    if not is_image and not is_video:
        return BaseResponse(
            code=400,
            message="请上传图片或视频文件。支持的图片格式：JPEG, PNG, GIF, WebP；支持的视频格式：MP4, AVI, MOV, WMV, FLV, WebM, MKV, 3GP",
            data=None
        )
    
    # 验证文件大小
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    # 根据文件类型设置不同的大小限制
    if is_image:
        max_file_size = getattr(settings, 'MAX_IMAGE_SIZE', 10 * 1024 * 1024)  # 图片默认10MB
        file_type_name = "图片"
    else:  # is_video
        max_file_size = getattr(settings, 'MAX_VIDEO_SIZE', 500 * 1024 * 1024)  # 视频默认500MB
        file_type_name = "视频"
    
    if file_size > max_file_size:
        return BaseResponse(
            code=400,
            message=f"{file_type_name}文件大小超过限制，最大允许 {max_file_size // (1024 * 1024)}MB",
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
        file_ext = os.path.splitext(filename)[1].lower()
        
        # 验证文件扩展名
        allowed_image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        allowed_video_exts = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.3gp']
        
        if is_image and file_ext not in allowed_image_exts:
            return BaseResponse(
                code=400,
                message=f"图片文件扩展名不支持，支持的扩展名：{', '.join(allowed_image_exts)}",
                data=None
            )
        elif is_video and file_ext not in allowed_video_exts:
            return BaseResponse(
                code=400,
                message=f"视频文件扩展名不支持，支持的扩展名：{', '.join(allowed_video_exts)}",
                data=None
            )
        
        # 如果没有扩展名，根据content_type添加默认扩展名
        if not file_ext:
            if is_image:
                if 'jpeg' in file.content_type or 'jpg' in file.content_type:
                    file_ext = '.jpg'
                elif 'png' in file.content_type:
                    file_ext = '.png'
                elif 'gif' in file.content_type:
                    file_ext = '.gif'
                elif 'webp' in file.content_type:
                    file_ext = '.webp'
                else:
                    file_ext = '.jpg'  # 默认
            else:  # is_video
                if 'mp4' in file.content_type:
                    file_ext = '.mp4'
                elif 'avi' in file.content_type:
                    file_ext = '.avi'
                elif 'mov' in file.content_type:
                    file_ext = '.mov'
                else:
                    file_ext = '.mp4'  # 默认
        
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
