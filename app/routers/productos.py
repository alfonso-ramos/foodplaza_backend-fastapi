from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.models import Producto, ProductoCreate, ProductoUpdate
from app.crud.productos import (
    get_producto,
    get_productos_by_menu,
    create_producto as crud_create_producto,
    update_producto as crud_update_producto,
    delete_producto as crud_delete_producto
)

router = APIRouter(prefix="", tags=["productos"])

@router.get("/{producto_id}", response_model=Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.get("/menu/{menu_id}", response_model=List[Producto])
def read_productos_by_menu(
    menu_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    solo_disponibles: bool = True,
    db: Session = Depends(get_db)
):
    return get_productos_by_menu(
        db=db, 
        menu_id=menu_id, 
        skip=skip, 
        limit=limit, 
        solo_disponibles=solo_disponibles
    )

@router.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crud_create_producto(db=db, producto=producto)

@router.put("/{producto_id}", response_model=Producto)
def update_producto(
    producto_id: int, 
    producto: ProductoUpdate, 
    db: Session = Depends(get_db)
):
    # Remove None values from the update data
    update_data = producto.dict(exclude_unset=True)
    
    # Check if there's anything to update
    if not update_data:
        raise HTTPException(
            status_code=400, 
            detail="No se proporcionaron datos para actualizar"
        )
    
    # Check if the product exists
    db_producto = get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Update the product
    updated_product = crud_update_producto(
        db, 
        producto_id=producto_id, 
        producto_data=update_data
    )
    
    return updated_product

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    success = crud_delete_producto(db, producto_id=producto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None
