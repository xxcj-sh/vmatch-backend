#!/usr/bin/env python3
"""
WeMatch 微信小程序服务端启动脚本
"""
import uvicorn
import os
import sys

def main():
    """启动应用"""
    # 添加当前目录到Python路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    # 启动FastAPI应用
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()