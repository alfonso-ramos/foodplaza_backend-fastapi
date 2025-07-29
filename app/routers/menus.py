from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models import Menu, MenuCreate
from app.crud.menus import (
    get_menu,
    get_menus_by_local,
    create_menu as crud_create_menu,
    update_menu as crud_update_menu,
    delete_menu as crud_delete_menu
)

router = APIRouter(prefix="", tags=["menus"])

@router.get("/{menu_id}", response_model=Menu)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    return db_menu

@router.get("/local/{local_id}", response_model=List[Menu])
def read_menus_by_local(local_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_menus_by_local(db, local_id=local_id, skip=skip, limit=limit)

@router.post("/", response_model=Menu, status_code=status.HTTP_201_CREATED)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    return crud_create_menu(db=db, menu=menu)

@router.put("/{menu_id}", response_model=Menu)
def update_menu(menu_id: int, menu: MenuCreate, db: Session = Depends(get_db)):
    db_menu = crud_update_menu(db, menu_id=menu_id, menu_data=menu.dict(exclude_unset=True))
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    return db_menu

@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    success = crud_delete_menu(db, menu_id=menu_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    return None
