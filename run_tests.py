#!/usr/bin/env python3
"""
测试运行脚本
"""
import subprocess
import sys
import os

def run_tests():
    """运行所有测试"""
    print("开始运行 WeMatch 微信小程序服务端测试...")
    
    # 确保在正确的目录下
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 运行pytest
    cmd = [sys.executable, "-m", "pytest", "-v", "tests/"]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 所有测试通过！")
        print("\n测试输出:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ 测试失败！")
        print("\n错误输出:")
        print(e.stderr)
        print("\n标准输出:")
        print(e.stdout)
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)