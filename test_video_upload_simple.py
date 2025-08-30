#!/usr/bin/env python3
"""
简化的视频文件上传测试
"""

from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_video_upload_with_auth():
    """使用认证测试视频文件上传"""
    
    print("测试视频文件上传功能（带认证）...")
    print("=" * 50)
    
    # 创建一个模拟的视频文件
    video_content = b"fake video content for testing"
    video_file = io.BytesIO(video_content)
    
    test_cases = [
        {
            "name": "MP4视频上传",
            "filename": "test_video.mp4",
            "content_type": "video/mp4"
        },
        {
            "name": "AVI视频上传", 
            "filename": "test_video.avi",
            "content_type": "video/avi"
        },
        {
            "name": "WebM视频上传",
            "filename": "test_video.webm",
            "content_type": "video/webm"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        
        # 重置文件指针
        video_file.seek(0)
        
        # 准备上传数据
        files = {
            "file": (test_case["filename"], video_file, test_case["content_type"])
        }
        data = {
            "type": "video"
        }
        
        # 使用测试token进行认证
        headers = {
            "Authorization": "Bearer test_token_001"
        }
        
        # 发送上传请求
        response = client.post(
            "/api/v1/files/upload",
            files=files,
            data=data,
            headers=headers
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 上传成功")
            print(f"响应: {result}")
            
            if result.get("code") == 0 and result.get("data", {}).get("url"):
                print(f"文件URL: {result['data']['url']}")
            else:
                print(f"❌ 响应格式错误: {result}")
        else:
            print(f"❌ 上传失败")
            print(f"响应: {response.text}")
        
        print("-" * 30)

def test_unsupported_file_types_with_auth():
    """测试不支持的文件类型（带认证）"""
    
    print("\n测试不支持的文件类型...")
    print("=" * 50)
    
    # 创建一个模拟的不支持的文件
    file_content = b"fake file content for testing"
    file_obj = io.BytesIO(file_content)
    
    unsupported_cases = [
        {
            "name": "文本文件",
            "filename": "test.txt",
            "content_type": "text/plain"
        },
        {
            "name": "音频文件",
            "filename": "test.mp3",
            "content_type": "audio/mpeg"
        }
    ]
    
    for i, test_case in enumerate(unsupported_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        
        # 重置文件指针
        file_obj.seek(0)
        
        # 准备上传数据
        files = {
            "file": (test_case["filename"], file_obj, test_case["content_type"])
        }
        data = {
            "type": "other"
        }
        
        # 使用测试token进行认证
        headers = {
            "Authorization": "Bearer test_token_001"
        }
        
        # 发送上传请求
        response = client.post(
            "/api/v1/files/upload",
            files=files,
            data=data,
            headers=headers
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") != 0:
                print("✅ 正确拒绝不支持的文件类型")
                print(f"错误信息: {result.get('message')}")
            else:
                print("❌ 应该拒绝不支持的文件类型")
        else:
            print(f"响应: {response.text}")
        
        print("-" * 30)

def test_image_upload_with_auth():
    """测试图片文件上传（确保原有功能正常）"""
    
    print("\n测试图片文件上传...")
    print("=" * 50)
    
    # 创建一个模拟的图片文件
    image_content = b"fake image content for testing"
    image_file = io.BytesIO(image_content)
    
    image_cases = [
        {
            "name": "JPEG图片上传",
            "filename": "test_image.jpg",
            "content_type": "image/jpeg"
        },
        {
            "name": "PNG图片上传",
            "filename": "test_image.png",
            "content_type": "image/png"
        }
    ]
    
    for i, test_case in enumerate(image_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        
        # 重置文件指针
        image_file.seek(0)
        
        # 准备上传数据
        files = {
            "file": (test_case["filename"], image_file, test_case["content_type"])
        }
        data = {
            "type": "image"
        }
        
        # 使用测试token进行认证
        headers = {
            "Authorization": "Bearer test_token_001"
        }
        
        # 发送上传请求
        response = client.post(
            "/api/v1/files/upload",
            files=files,
            data=data,
            headers=headers
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 上传成功")
            print(f"响应: {result}")
            
            if result.get("code") == 0 and result.get("data", {}).get("url"):
                print(f"文件URL: {result['data']['url']}")
            else:
                print(f"❌ 响应格式错误: {result}")
        else:
            print(f"❌ 上传失败")
            print(f"响应: {response.text}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_video_upload_with_auth()
    test_unsupported_file_types_with_auth()
    test_image_upload_with_auth()
    print("\n测试完成！")