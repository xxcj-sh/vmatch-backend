import pytest
from fastapi.testclient import TestClient
from io import BytesIO

class TestFile:
    """测试文件上传相关接口"""
    
    def test_upload_image_success(self, client: TestClient, auth_headers: dict):
        """测试上传图片成功"""
        # 创建测试图片
        test_image = BytesIO(b"fake image data")
        test_image.name = "test.jpg"
        
        response = client.post(
            "/api/v1/file/upload",
            files={"file": ("test.jpg", test_image, "image/jpeg")},
            data={"type": "avatar"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "url" in data["data"]
    
    def test_upload_non_image_file(self, client: TestClient, auth_headers: dict):
        """测试上传非图片文件"""
        test_file = BytesIO(b"fake text data")
        test_file.name = "test.txt"
        
        response = client.post(
            "/api/v1/file/upload",
            files={"file": ("test.txt", test_file, "text/plain")},
            data={"type": "avatar"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 400
        assert data["message"] == "请上传图片文件"