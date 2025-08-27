from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.utils.db_config import get_db
from app.services import db_service
from app.services.mock_data import mock_data_service

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
    responses={404: {"description": "Not found"}},
)

# 匹配详情模型
class MatchDetailBase(BaseModel):
    detail_type: str
    detail_value: str

class MatchDetailCreate(MatchDetailBase):
    pass

class MatchDetail(MatchDetailBase):
    id: int
    match_id: int

    class Config:
        orm_mode = True

# 匹配模型
class MatchBase(BaseModel):
    user_id: int
    match_type: str
    status: str
    score: float = 0.0

class MatchCreate(MatchBase):
    details: List[MatchDetailCreate] = []

class MatchUpdate(BaseModel):
    match_type: Optional[str] = None
    status: Optional[str] = None
    score: Optional[float] = None
    is_active: Optional[bool] = None

class Match(MatchBase):
    id: int
    is_active: bool
    details: List[MatchDetail] = []

    class Config:
        orm_mode = True

# 路由
@router.post("/", response_model=Match, status_code=status.HTTP_201_CREATED)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    # 检查用户是否存在
    user = db_service.get_user(db, user_id=match.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    match_data = match.dict(exclude={"details"})
    details = match.details
    
    db_match = db_service.create_match(db=db, match_data=match_data, details=[d.dict() for d in details])
    
    # 获取完整的匹配信息，包括详情
    result = db_service.get_match(db, match_id=db_match.id)
    return result

@router.get("/", response_model=List[Match])
def read_matches(user_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    matches = db_service.get_matches(db, user_id=user_id, skip=skip, limit=limit)
    return matches

# 符合文档的匹配卡片端点，需优先于动态路由
@router.get("/cards")
def get_match_cards(
    matchType: str = Query(...),
    userRole: str = Query(...),
    page: int = Query(1),
    pageSize: int = Query(10)
):
    result = mock_data_service.get_cards(
        match_type=matchType, user_role=userRole, page=page, page_size=pageSize
    )
    return {
        "code": 0,
        "message": "success",
        "data": {
            "cards": result["list"],
            "pagination": {
                "page": result["page"],
                "pageSize": result["pageSize"],
                "total": result["total"],
                "hasMore": result["page"] * result["pageSize"] < result["total"],
            },
        },
    }

@router.get("/{match_id}", response_model=Match)
def read_match(match_id: int, db: Session = Depends(get_db)):
    db_match = db_service.get_match(db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match

@router.put("/{match_id}", response_model=Match)
def update_match(match_id: int, match: MatchUpdate, db: Session = Depends(get_db)):
    db_match = db_service.update_match(db, match_id=match_id, match_data=match.dict(exclude_unset=True))
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match

@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    success = db_service.delete_match(db, match_id=match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"detail": "Match deleted"}

# 匹配详情路由
@router.post("/{match_id}/details", response_model=MatchDetail)
def add_match_detail(match_id: int, detail: MatchDetailCreate, db: Session = Depends(get_db)):
    # 检查匹配是否存在
    match = db_service.get_match(db, match_id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return db_service.add_match_detail(db, match_id=match_id, detail_data=detail.dict())

@router.get("/{match_id}/details", response_model=List[MatchDetail])
def read_match_details(match_id: int, db: Session = Depends(get_db)):
    # 检查匹配是否存在
    match = db_service.get_match(db, match_id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return db_service.get_match_details(db, match_id=match_id)