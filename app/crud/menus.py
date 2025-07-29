from sqlalchemy.orm import Session
from ..models import MenuDB, MenuCreate, Menu

def get_menu(db: Session, menu_id: int):
    return db.query(MenuDB).filter(MenuDB.id == menu_id).first()

def get_menus_by_local(db: Session, local_id: int, skip: int = 0, limit: int = 100):
    return db.query(MenuDB).filter(MenuDB.id_local == local_id).offset(skip).limit(limit).all()

def create_menu(db: Session, menu: MenuCreate):
    db_menu = MenuDB(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def update_menu(db: Session, menu_id: int, menu_data: dict):
    db_menu = db.query(MenuDB).filter(MenuDB.id == menu_id).first()
    if not db_menu:
        return None
    
    for key, value in menu_data.items():
        setattr(db_menu, key, value)
    
    db.commit()
    db.refresh(db_menu)
    return db_menu

def delete_menu(db: Session, menu_id: int):
    db_menu = db.query(MenuDB).filter(MenuDB.id == menu_id).first()
    if not db_menu:
        return False
    
    db.delete(db_menu)
    db.commit()
    return True
