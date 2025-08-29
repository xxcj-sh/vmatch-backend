from sqlalchemy import Column, String, Integer, Text, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.db_config import Base

class UserProfile(Base):
    """用户角色资料表 - 同一用户可以有多个不同角色的资料"""
    __tablename__ = "user_profiles"

    id = Column(String, primary_key=True, index=True)  # 资料ID
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)  # 用户ID
    role_type = Column(String, nullable=False, index=True)  # 角色类型：housing_seeker, housing_provider, dating_seeker, activity_organizer等
    scene_type = Column(String, nullable=False, index=True)  # 场景类型：housing, dating, activity
    
    # 基础信息
    display_name = Column(String, nullable=False)  # 显示名称
    avatar_url = Column(String, nullable=True)  # 头像URL
    bio = Column(Text, nullable=True)  # 个人简介
    
    # 详细资料 - 使用JSON存储不同角色的特定信息
    profile_data = Column(JSON, nullable=True)  # 角色特定数据
    preferences = Column(JSON, nullable=True)  # 偏好设置
    tags = Column(JSON, nullable=True)  # 标签列表
    
    # 状态信息
    is_active = Column(Integer, default=1)  # 是否激活 1-激活 0-停用
    visibility = Column(String, default="public")  # 可见性：public, private, friends
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="profiles")

# 更新User模型以添加profiles关系