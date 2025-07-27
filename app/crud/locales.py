from sqlalchemy.orm import Session
from ..models import LocaleDB

def get_locale(db: Session, locale_id: int):
    return db.query(LocaleDB).filter(LocaleDB.id == locale_id).first()

def get_locales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LocaleDB).offset(skip).limit(limit).all()

def create_locale(db: Session, locale):
    db_locale = LocaleDB(**locale.dict())
    db.add(db_locale)
    db.commit()
    db.refresh(db_locale)
    return db_locale

def update_locale(db: Session, locale_id: int, locale_data):
    db_locale = db.query(LocaleDB).filter(LocaleDB.id == locale_id).first()
    if not db_locale:
        return None
    
    for key, value in locale_data.dict().items():
        setattr(db_locale, key, value)
    
    db.commit()
    db.refresh(db_locale)
    return db_locale

def delete_locale(db: Session, locale_id: int):
    db_locale = db.query(LocaleDB).filter(LocaleDB.id == locale_id).first()
    if not db_locale:
        return False
    
    db.delete(db_locale)
    db.commit()
    return True