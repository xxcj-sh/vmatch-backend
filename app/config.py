from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "WeMatch 微信小程序服务端"
    debug: bool = True
    
    # 安全配置
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 120  # 2小时
    
    # 数据库配置（测试模式使用内存数据）
    database_url: str = "sqlite:///./wematch.db"
    
    # 微信配置
    wx_app_id: str = "your-wx-app-id"
    wx_app_secret: str = "your-wx-app-secret"
    
    # 文件上传配置
    upload_dir: str = "./uploads"
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    
    # 测试模式
    test_mode: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()