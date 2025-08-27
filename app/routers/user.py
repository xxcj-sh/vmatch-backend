from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from app.utils.db_config import get_db
from app.services import db_service
from app.services.data_adapter import data_service
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# 用户模型
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    is_active: bool = None

class ProfileUpdate(BaseModel):
    nickName: str = None
    avatarUrl: str = None
    gender: int = None
    age: int = None
    occupation: str = None
    location: list = None
    bio: str = None
    matchType: str = None
    userRole: str = None
    interests: list = None
    preferences: dict = None
    phone: str = None
    education: str = None

class User(UserBase):
    id: str
    is_active: bool

    class Config:
        orm_mode = True

# 路由
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 在实际应用中，这里应该对密码进行哈希处理
    hashed_password = user.password  # 简化示例，实际应使用哈希
    
    user_data = user.dict()
    user_data.pop("password")
    user_data["hashed_password"] = hashed_password
    
    return db_service.create_user(db=db, user_data=user_data)

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/me")
def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.put("/me")
def update_current_user(profile_data: ProfileUpdate, current_user: Dict[str, Any] = Depends(get_current_user)):
    """更新当前用户信息"""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # 转换为字典，排除未设置的字段
    update_dict = profile_data.dict(exclude_unset=True)
    
    updated_user = data_service.update_profile(user_id, update_dict)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.get("/me/stats")
def get_current_user_stats(current_user: Dict[str, Any] = Depends(get_current_user)):
    """获取用户统计信息"""
    return {
        "code": 0,
        "message": "success",
        "data": {
            "matchCount": 10,
            "messageCount": 50,
            "favoriteCount": 5
        }
    }

@router.get("/{user_id}", response_model=User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db_service.update_user(db, user_id=user_id, user_data=user.dict(exclude_unset=True))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    success = db_service.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


