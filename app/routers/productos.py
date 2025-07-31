from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.schemas.productos import Producto, ProductoCreate, ProductoUpdate
from app.crud.productos import (
    get_producto,
    get_productos_by_menu,
    create_producto as crud_create_producto,
    update_producto as crud_update_producto,
    delete_producto as crud_delete_producto
)

router = APIRouter(prefix="", tags=["productos"])

@router.get("/{producto_id}", response_model=Producto, summary="Get a product by ID", description="Get a single product by its ID.")
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto específico por su ID.
    """
    db_producto = get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_producto

@router.get("/menu/{menu_id}", response_model=List[Producto], summary="Get all products for a menu", description="Get a list of all products for a specific menu.")
def read_productos_by_menu(
    menu_id: int, 
    skip: int = Query(0, ge=0, description="Number of records to skip"), 
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    disponible: Optional[bool] = Query(None, description="Filter by availability"),
    nombre: Optional[str] = Query(None, description="Filter by name (partial search)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista de productos para un menú específico con opciones de filtrado.
    """
    return get_productos_by_menu(
        db=db,
        menu_id=menu_id, 
        skip=skip, 
        limit=limit, 
        disponible=disponible,
        nombre=nombre
    )

@router.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED, summary="Create a new product", description="Create a new product with the provided data.")
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo producto.
    """
    return crud_create_producto(db=db, producto=producto)

@router.put("/{producto_id}", response_model=Producto, summary="Update a product", description="Update an existing product's data.")
def update_producto(
    producto_id: int, 
    producto: ProductoUpdate, 
    db: Session = Depends(get_db)
):
    """
    Actualiza un producto existente.
    """
    db_producto = crud_update_producto(db, producto_id=producto_id, producto_data=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_producto

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a product", description="Delete a product by its ID.")
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    success = crud_delete_producto(db, producto_id=producto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
