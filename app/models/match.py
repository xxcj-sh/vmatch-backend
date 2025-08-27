from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.db_config import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(String, primary_key=True, index=True)  # 改为String类型支持字符串ID
    user_id = Column(String, ForeignKey("users.id"))  # 改为String类型匹配用户ID
    match_type = Column(String)
    status = Column(String)
    score = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="matches")
    match_details = relationship("MatchDetail", back_populates="match")

class MatchDetail(Base):
    __tablename__ = "match_details"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.id"))  # 改为String类型匹配match ID
    detail_type = Column(String)
    detail_value = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    match = relationship("Match", back_populates="match_details")
