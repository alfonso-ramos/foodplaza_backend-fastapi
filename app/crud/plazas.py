from sqlalchemy.orm import Session
from ..models import PlazaDB

def get_plaza(db: Session, plaza_id: int):
    return db.query(PlazaDB).filter(PlazaDB.id == plaza_id).first()

def get_plazas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PlazaDB).offset(skip).limit(limit).all()

def create_plaza(db: Session, plaza):
    db_plaza = PlazaDB(**plaza.dict())
    db.add(db_plaza)
    db.commit()
    db.refresh(db_plaza)
    return db_plaza

def update_plaza(db: Session, plaza_id: int, plaza_data):
    db_plaza = db.query(PlazaDB).filter(PlazaDB.id == plaza_id).first()
    if not db_plaza:
        return None
    
    # plaza_data ya es un diccionario, no necesitamos llamar a .dict()
    for key, value in plaza_data.items():
        setattr(db_plaza, key, value)
    
    db.commit()
    db.refresh(db_plaza)
    return db_plaza

def delete_plaza(db: Session, plaza_id: int):
    db_plaza = db.query(PlazaDB).filter(PlazaDB.id == plaza_id).first()
    if not db_plaza:
        return False
    
    db.delete(db_plaza)
    db.commit()
    return True
