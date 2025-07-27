from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.models import Locale, LocaleCreate
from app.crud.locales import (
    get_locale,
    get_locales,
    create_locale as crud_create_locale,
    update_locale as crud_update_locale,
    delete_locale as crud_delete_locale
)

router = APIRouter(prefix="", tags=["locales"])

@router.get("/{locale_id}", response_model=Locale)
def read_locale(locale_id: int, db: Session = Depends(get_db)):
    db_locale = get_locale(db, locale_id=locale_id)
    if db_locale is None:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    return db_locale

@router.get("/", response_model=List[Locale])
def read_locales(
    skip: int = 0, 
    limit: int = 100, 
    plaza_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return get_locales(db, skip=skip, limit=limit, plaza_id=plaza_id)

@router.post("/", response_model=Locale, status_code=status.HTTP_201_CREATED)
def create_new_locale(locale: LocaleCreate, db: Session = Depends(get_db)):
    return crud_create_locale(db=db, locale=locale)

@router.put("/{locale_id}", response_model=Locale)
def update_locale(locale_id: int, locale: LocaleCreate, db: Session = Depends(get_db)):
    db_locale = crud_update_locale(
        db, 
        locale_id=locale_id, 
        locale_data=locale.dict(exclude_unset=True)
    )
    if db_locale is None:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    return db_locale

@router.delete("/{locale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_locale(locale_id: int, db: Session = Depends(get_db)):
    success = crud_delete_locale(db, locale_id=locale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    return None
