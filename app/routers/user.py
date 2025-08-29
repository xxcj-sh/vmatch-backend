from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from app.utils.db_config import get_db
from app.services import db_service
from app.services.data_adapter import data_service
from app.services.user_profile_service import UserProfileService
from app.dependencies import get_current_user
from app.models.user_profile_schemas import (
    UserProfileCreate, UserProfileUpdate, UserProfile as UserProfileSchema,
    UserAllProfilesResponse
)
from app.utils.db_config import get_db

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

@router.get("/me/profiles", response_model=UserAllProfilesResponse)
def get_current_user_profiles(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的所有角色资料"""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    return UserProfileService.get_user_all_profiles_response(db, user_id)

@router.get("/me/profiles/{scene_type}")
def get_current_user_profiles_by_scene(
    scene_type: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户在特定场景下的角色资料"""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    profiles = UserProfileService.get_profiles_by_scene(db, user_id, scene_type)
    return {
        "code": 0,
        "message": "success",
        "data": {
            "scene_type": scene_type,
            "profiles": profiles
        }
    }

@router.get("/me/profiles/{scene_type}/{role_type}")
def get_current_user_profile_by_role(
    scene_type: str,
    role_type: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户在特定场景和角色下的资料"""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    profile = UserProfileService.get_user_profile_by_role(db, user_id, scene_type, role_type)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return {
        "code": 0,
        "message": "success",
        "data": profile
    }

@router.post("/me/profiles", response_model=UserProfileSchema)
def create_user_profile(
    profile_data: UserProfileCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建用户角色资料"""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # 检查是否已存在相同场景和角色的资料
    existing_profile = UserProfileService.get_user_profile_by_role(
        db, user_id, profile_data.scene_type, profile_data.role_type
    )
    if existing_profile:
        raise HTTPException(
            status_code=400, 
            detail=f"Profile for {profile_data.scene_type}.{profile_data.role_type} already exists"
        )
    
    return UserProfileService.create_profile(db, user_id, profile_data)

@router.put("/me/profiles/{profile_id}")
def update_user_profile(
    profile_id: str,
    update_data: UserProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户角色资料"""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # 验证资料属于当前用户
    profile = UserProfileService.get_profile_by_id(db, profile_id)
    if not profile or profile.user_id != user_id:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    updated_profile = UserProfileService.update_profile(db, profile_id, update_data)
    return {
        "code": 0,
        "message": "success",
        "data": updated_profile
    }

@router.delete("/me/profiles/{profile_id}")
def delete_user_profile(
    profile_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除用户角色资料"""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # 验证资料属于当前用户
    profile = UserProfileService.get_profile_by_id(db, profile_id)
    if not profile or profile.user_id != user_id:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    success = UserProfileService.delete_profile(db, profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return {
        "code": 0,
        "message": "Profile deleted successfully"
    }

@router.patch("/me/profiles/{profile_id}/toggle")
def toggle_user_profile_status(
    profile_id: str,
    is_active: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """切换用户角色资料的激活状态"""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # 验证资料属于当前用户
    profile = UserProfileService.get_profile_by_id(db, profile_id)
    if not profile or profile.user_id != user_id:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    updated_profile = UserProfileService.toggle_profile_status(db, profile_id, is_active)
    return {
        "code": 0,
        "message": "Profile status updated successfully",
        "data": updated_profile
    }

@router.get("/{user_id}/profiles/{scene_type}/{role_type}")
def get_user_profile_by_role(
    user_id: str,
    scene_type: str,
    role_type: str,
    db: Session = Depends(get_db)
):
    """获取指定用户在特定场景和角色下的资料"""
    # 首先尝试作为用户ID查询
    profile = UserProfileService.get_user_profile_by_role(db, user_id, scene_type, role_type)
    
    # 如果没找到，检查user_id是否实际上是一个profile_id
    if not profile:
        # 尝试通过profile_id获取profile
        profile_by_id = UserProfileService.get_profile_by_id(db, user_id)
        if profile_by_id:
            # 获取完整的用户资料信息
            full_profile = UserProfileService.get_user_profile_by_role(
                db, profile_by_id.user_id, profile_by_id.scene_type, profile_by_id.role_type
            )
            if full_profile:
                # 返回找到的profile，说明实际的类型
                return {
                    "code": 0,
                    "message": f"Found profile by ID: {profile_by_id.scene_type}.{profile_by_id.role_type}",
                    "requested": {"scene_type": scene_type, "role_type": role_type},
                    "actual": {"scene_type": profile_by_id.scene_type, "role_type": profile_by_id.role_type},
                    "data": full_profile
                }
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return {
        "code": 0,
        "message": "success",
        "data": profile
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


