import os
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.db_config import Base
from app.models import User, Match, MatchDetail

def export_data(source_db_url, output_file="migration_data.json"):
    """从源数据库导出数据到JSON文件"""
    # 连接源数据库
    engine = create_engine(source_db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 导出数据
    data = {
        "users": [],
        "matches": [],
        "match_details": []
    }
    
    # 导出用户
    users = session.query(User).all()
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
        data["users"].append(user_data)
    
    # 导出匹配
    matches = session.query(Match).all()
    for match in matches:
        match_data = {
            "id": match.id,
            "user_id": match.user_id,
            "match_type": match.match_type,
            "status": match.status,
            "score": match.score,
            "is_active": match.is_active,
            "created_at": match.created_at.isoformat() if match.created_at else None,
            "updated_at": match.updated_at.isoformat() if match.updated_at else None
        }
        data["matches"].append(match_data)
    
    # 导出匹配详情
    match_details = session.query(MatchDetail).all()
    for detail in match_details:
        detail_data = {
            "id": detail.id,
            "match_id": detail.match_id,
            "detail_type": detail.detail_type,
            "detail_value": detail.detail_value,
            "created_at": detail.created_at.isoformat() if detail.created_at else None
        }
        data["match_details"].append(detail_data)
    
    # 保存到JSON文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已导出到 {output_file}")
    session.close()

def import_data(target_db_url, input_file="migration_data.json"):
    """从JSON文件导入数据到目标数据库"""
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：文件 {input_file} 不存在")
        return False
    
    # 加载数据
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 连接目标数据库
    engine = create_engine(target_db_url)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # 导入用户
        for user_data in data["users"]:
            # 处理日期字段
            if user_data.get("created_at"):
                user_data["created_at"] = datetime.fromisoformat(user_data["created_at"])
            if user_data.get("updated_at"):
                user_data["updated_at"] = datetime.fromisoformat(user_data["updated_at"])
            
            # 检查用户是否已存在
            existing_user = session.query(User).filter(User.id == user_data["id"]).first()
            if existing_user:
                # 更新现有用户
                for key, value in user_data.items():
                    setattr(existing_user, key, value)
            else:
                # 创建新用户
                user = User(**user_data)
                session.add(user)
        
        # 导入匹配
        for match_data in data["matches"]:
            # 处理日期字段
            if match_data.get("created_at"):
                match_data["created_at"] = datetime.fromisoformat(match_data["created_at"])
            if match_data.get("updated_at"):
                match_data["updated_at"] = datetime.fromisoformat(match_data["updated_at"])
            
            # 检查匹配是否已存在
            existing_match = session.query(Match).filter(Match.id == match_data["id"]).first()
            if existing_match:
                # 更新现有匹配
                for key, value in match_data.items():
                    setattr(existing_match, key, value)
            else:
                # 创建新匹配
                match = Match(**match_data)
                session.add(match)
        
        # 导入匹配详情
        for detail_data in data["match_details"]:
            # 处理日期字段
            if detail_data.get("created_at"):
                detail_data["created_at"] = datetime.fromisoformat(detail_data["created_at"])
            
            # 检查详情是否已存在
            existing_detail = session.query(MatchDetail).filter(MatchDetail.id == detail_data["id"]).first()
            if existing_detail:
                # 更新现有详情
                for key, value in detail_data.items():
                    setattr(existing_detail, key, value)
            else:
                # 创建新详情
                detail = MatchDetail(**detail_data)
                session.add(detail)
        
        # 提交所有更改
        session.commit()
        print("数据导入成功")
        return True
    
    except Exception as e:
        session.rollback()
        print(f"导入数据时出错：{e}")
        return False
    
    finally:
        session.close()

def migrate_database(source_db_url, target_db_url, temp_file="migration_data.json"):
    """将数据从源数据库迁移到目标数据库"""
    print(f"开始从 {source_db_url} 迁移数据到 {target_db_url}")
    
    # 导出数据
    export_data(source_db_url, temp_file)
    
    # 导入数据
    success = import_data(target_db_url, temp_file)
    
    # 清理临时文件
    if os.path.exists(temp_file) and success:
        os.remove(temp_file)
        print(f"临时文件 {temp_file} 已删除")
    
    if success:
        print("数据库迁移完成")
    else:
        print("数据库迁移失败")
    
    return success

if __name__ == "__main__":
    # 示例用法
    # 从SQLite迁移到PostgreSQL
    # migrate_database(
    #     "sqlite:///./vmatch_dev.db",
    #     "postgresql://user:password@localhost/vmatch"
    # )
    
    # 或者只导出数据
    # export_data("sqlite:///./vmatch_dev.db", "backup_data.json")
    
    # 或者只导入数据
    # import_data("postgresql://user:password@localhost/vmatch", "backup_data.json")
    
    print("请在代码中取消注释相应的函数调用来执行迁移操作")