from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import locales as crud_locales
from ..models.locales import LocalDB
from ..schemas.locales import Locale, LocaleCreate

router = APIRouter(prefix="", tags=["locales"])

@router.get("/", response_model=list[Locale])
def list_locales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_locales(db, skip=skip, limit=limit)

@router.get("/{locale_id}", response_model=Locale)
def read_locale(locale_id: int, db: Session = Depends(get_db)):
    db_locale = get_locale(db, locale_id=locale_id)
    if not db_locale:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    return db_locale

@router.post("/", response_model=Locale, status_code=status.HTTP_201_CREATED)
def create_new_locale(locale: LocaleCreate, db: Session = Depends(get_db)):
    return create_locale(db=db, locale=locale)

@router.put("/{locale_id}", response_model=Locale)
def update_existing_locale(locale_id: int, locale: LocaleCreate, db: Session = Depends(get_db)):
    db_locale = update_locale(db, locale_id=locale_id, locale_data=locale)
    if not db_locale:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    return db_locale

@router.delete("/{locale_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_locale(locale_id: int, db: Session = Depends(get_db)):
    success = crud_locales.delete_locale(db, locale_id=locale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    return None