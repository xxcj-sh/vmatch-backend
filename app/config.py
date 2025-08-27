import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class Settings(BaseSettings):
    """应用配置"""
    # 环境设置
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # 数据库配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///./vmatch_{ENVIRONMENT}.db"
    )
    
    # 应用配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 测试模式配置 - 默认关闭
    test_mode: bool = os.getenv("TEST_MODE", "false").lower() == "true"
    
    # 文件上传配置
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    upload_dir: str = UPLOAD_DIR  # 兼容性别名
    
    class Config:
        env_file = ".env"

# 创建设置实例
settings = Settings()