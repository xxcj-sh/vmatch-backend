from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.db_config import get_db
from app.services.user_profile_service import UserProfileService

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{profile_id}/details")
def get_profile_details(
    profile_id: str,
    db: Session = Depends(get_db)
):
    """通过profile ID获取资料详情"""
    profile = UserProfileService.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # 获取完整的用户资料信息
    full_profile = UserProfileService.get_user_profile_by_role(
        db, profile.user_id, profile.scene_type, profile.role_type
    )
    
    if not full_profile:
        raise HTTPException(status_code=404, detail="Profile details not found")
    
    return {
        "code": 0,
        "message": "success",
        "data": full_profile
    }