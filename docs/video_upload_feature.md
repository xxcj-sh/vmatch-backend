# 视频文件上传功能实现

## 功能概述
已成功为文件上传接口添加了视频格式支持，现在支持图片和视频两种文件类型的上传。

## 支持的文件格式

### 图片格式
- **JPEG** (.jpg, .jpeg) - `image/jpeg`
- **PNG** (.png) - `image/png`
- **GIF** (.gif) - `image/gif`
- **WebP** (.webp) - `image/webp`
- **文件大小限制**: 10MB

### 视频格式
- **MP4** (.mp4) - `video/mp4`
- **AVI** (.avi) - `video/avi`
- **MOV** (.mov) - `video/mov`
- **WMV** (.wmv) - `video/wmv`
- **FLV** (.flv) - `video/flv`
- **WebM** (.webm) - `video/webm`
- **MKV** (.mkv) - `video/mkv`
- **3GP** (.3gp) - `video/3gp`
- **文件大小限制**: 500MB

## API接口

### 上传文件
```http
POST /api/v1/files/upload
Content-Type: multipart/form-data
Authorization: Bearer {token}
```

**请求参数:**
- `file` (required): 要上传的文件
- `type` (required): 文件类型标识（如 "image", "video"）

**响应格式:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "url": "/uploads/uuid-filename.ext"
  }
}
```

**错误响应:**
```json
{
  "code": 400,
  "message": "请上传图片或视频文件。支持的图片格式：JPEG, PNG, GIF, WebP；支持的视频格式：MP4, AVI, MOV, WMV, FLV, WebM, MKV, 3GP",
  "data": null
}
```

## 实现细节

### 1. 文件类型验证
- 通过 `content_type` 验证文件MIME类型
- 通过文件扩展名进行二次验证
- 支持无扩展名文件，会根据MIME类型自动添加扩展名

### 2. 文件大小限制
- 图片文件：最大10MB (`MAX_IMAGE_SIZE`)
- 视频文件：最大500MB (`MAX_VIDEO_SIZE`)
- 可通过配置文件或环境变量调整

### 3. 文件存储
- 使用UUID生成唯一文件名，避免文件名冲突
- 保持原始文件扩展名
- 存储在配置的上传目录中

### 4. 安全性
- 严格的文件类型验证
- 文件大小限制防止滥用
- 唯一文件名防止覆盖

## 配置项

在 `app/config.py` 中添加了以下配置：

```python
# 文件大小限制配置
MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB (通用限制)
MAX_IMAGE_SIZE: int = 10 * 1024 * 1024   # 10MB (图片限制)
MAX_VIDEO_SIZE: int = 500 * 1024 * 1024  # 500MB (视频限制)
```

可通过环境变量覆盖：
```bash
MAX_IMAGE_SIZE=20971520  # 20MB
MAX_VIDEO_SIZE=1073741824  # 1GB
```

## 测试结果

### ✅ 成功测试用例
1. **MP4视频上传** - 状态码200，返回文件URL
2. **AVI视频上传** - 状态码200，返回文件URL
3. **WebM视频上传** - 状态码200，返回文件URL
4. **JPEG图片上传** - 状态码200，返回文件URL
5. **PNG图片上传** - 状态码200，返回文件URL

### ✅ 错误处理测试
1. **不支持的文件类型** - 正确拒绝并返回错误信息
2. **文件大小超限** - 正确拒绝并返回大小限制信息
3. **无效文件扩展名** - 正确拒绝并返回支持的扩展名列表

## 使用示例

### JavaScript/前端上传
```javascript
const formData = new FormData();
formData.append('file', videoFile);
formData.append('type', 'video');

fetch('/api/v1/files/upload', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token
  },
  body: formData
})
.then(response => response.json())
.then(data => {
  if (data.code === 0) {
    console.log('上传成功:', data.data.url);
  } else {
    console.error('上传失败:', data.message);
  }
});
```

### Python测试代码
```python
import requests

files = {'file': ('video.mp4', open('video.mp4', 'rb'), 'video/mp4')}
data = {'type': 'video'}
headers = {'Authorization': 'Bearer your_token'}

response = requests.post(
    'http://localhost:8000/api/v1/files/upload',
    files=files,
    data=data,
    headers=headers
)

print(response.json())
```

## 注意事项

1. **认证要求**: 所有文件上传都需要有效的Bearer token
2. **存储空间**: 视频文件较大，需要确保服务器有足够的存储空间
3. **网络传输**: 大文件上传可能需要较长时间，建议前端添加进度显示
4. **文件清理**: 建议定期清理未使用的上传文件
5. **CDN集成**: 生产环境建议集成CDN服务来优化文件访问速度

## 后续优化建议

1. **分片上传**: 对于大视频文件，可以实现分片上传功能
2. **视频压缩**: 可以集成视频压缩服务来减少存储空间
3. **缩略图生成**: 自动为视频生成缩略图
4. **文件预览**: 添加视频文件的在线预览功能
5. **云存储集成**: 集成阿里云OSS、腾讯云COS等云存储服务