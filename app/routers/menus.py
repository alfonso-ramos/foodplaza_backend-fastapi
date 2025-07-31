from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.schemas.menus import Menu, MenuCreate, MenuUpdate
from app.crud.menus import (
    get_menu,
    get_menus_by_local,
    create_menu as crud_create_menu,
    update_menu as crud_update_menu,
    delete_menu as crud_delete_menu
)

router = APIRouter(prefix="", tags=["menus"])

@router.get("/{menu_id}", response_model=Menu, summary="Get a menu by ID", description="Get a single menu by its ID.")
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un menú específico por su ID.
    """
    db_menu = get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu

@router.get("/local/{local_id}", response_model=List[Menu], summary="Get all menus for a locale", description="Get a list of all menus for a specific locale.")
def read_menus_by_local(
    local_id: int, 
    skip: int = Query(0, ge=0, description="Number of records to skip"), 
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    nombre: Optional[str] = Query(None, description="Filter by name (partial search)"),
    disponible: Optional[bool] = Query(None, description="Filter by availability"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista de menús para un local específico con opciones de filtrado.
    """
    return get_menus_by_local(
        db, 
        local_id=local_id, 
        skip=skip, 
        limit=limit,
        nombre=nombre,
        disponible=disponible
    )

@router.post("/", response_model=Menu, status_code=status.HTTP_201_CREATED, summary="Create a new menu", description="Create a new menu with the provided data.")
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo menú.
    """
    return crud_create_menu(db=db, menu=menu)

@router.put("/{menu_id}", response_model=Menu, summary="Update a menu", description="Update an existing menu's data.")
def update_menu(
    menu_id: int, 
    menu: MenuUpdate, 
    db: Session = Depends(get_db)
):
    """
    Actualiza un menú existente.
    """
    db_menu = crud_update_menu(db, menu_id=menu_id, menu_data=menu)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu

@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a menu", description="Delete a menu by its ID.")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """
    Elimina un menú por su ID.
    """
    success = crud_delete_menu(db, menu_id=menu_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu not found")
    return None
