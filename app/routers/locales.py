from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.models import Locale, LocaleCreate, UsuarioDB
from app.crud.locales import (
    get_locale,
    get_locales,
    create_locale as crud_create_locale,
    update_locale as crud_update_locale,
    delete_locale as crud_delete_locale
)
from app.crud import usuarios as crud_usuarios

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
    tipo_comercio: Optional[str] = None,
    id_gerente: Optional[int] = None,
    db: Session = Depends(get_db)
):
    # Validar que el tipo de comercio sea válido si se proporciona
    if tipo_comercio:
        tipos_validos = ['restaurante', 'cafeteria', 'tienda', 'servicio', 'otro']
        if tipo_comercio.lower() not in tipos_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de comercio no válido. Debe ser uno de: {', '.join(tipos_validos)}"
            )
    
    # Validar que el gerente exista si se proporciona
    if id_gerente is not None:
        gerente = db.query(UsuarioDB).filter(
            UsuarioDB.id == id_gerente,
            UsuarioDB.rol == 'gerente',
            UsuarioDB.estado == 'activo'
        ).first()
        if not gerente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID de gerente proporcionado no es válido o el usuario no tiene permisos de gerente"
            )
    
    return get_locales(
        db, 
        skip=skip, 
        limit=limit, 
        plaza_id=plaza_id,
        tipo_comercio=tipo_comercio,
        id_gerente=id_gerente
    )

@router.post("/", response_model=Locale, status_code=status.HTTP_201_CREATED)
def create_new_locale(locale: LocaleCreate, db: Session = Depends(get_db)):
    try:
        return crud_create_locale(db=db, locale=locale)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{locale_id}", response_model=Locale)
def update_locale(locale_id: int, locale: LocaleCreate, db: Session = Depends(get_db)):
    try:
        db_locale = crud_update_locale(
            db, 
            locale_id=locale_id, 
            locale_data=locale
        )
        if db_locale is None:
            raise HTTPException(status_code=404, detail="Local no encontrado")
        return db_locale
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{locale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_locale(locale_id: int, db: Session = Depends(get_db)):
    success = crud_delete_locale(db, locale_id=locale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    return None
