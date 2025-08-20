#!/usr/bin/env python3
"""
测试新的视频URL列表
"""
import json
import urllib.request
from app.utils.test_data_generator import TestDataGenerator

def test_video_urls():
    """测试视频URL列表"""
    print("🔍 测试新的视频URL列表")
    print("=" * 50)
    
    # 预定义的可访问视频URL列表
    working_video_urls = [
    "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
    "https://www.w3schools.com/html/mov_bbb.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4"
]
    
    print("✅ 可用的视频URL列表:")
    for i, url in enumerate(working_video_urls, 1):
        print(f"{i:2d}. {url}")
    
    print("\n" + "=" * 50)
    print("🔍 生成测试房源数据:")
    
    # 生成几个房源数据并显示视频URL
    for i in range(3):
        house_info = TestDataGenerator.generate_house_info()
        video_url = house_info["videoUrl"]
        print(f"\n房源 {i+1}: {video_url}")
        
        # 检查是否在可用列表中
        if video_url in working_video_urls:
            print("  ✅ 在可用列表中")
        else:
            print("  ❌ 不在可用列表中")

if __name__ == "__main__":
    test_video_urls()