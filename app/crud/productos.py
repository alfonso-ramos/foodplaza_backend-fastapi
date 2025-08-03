from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException
from .. import models, schemas
from ..models import ProductoDB, ProductoCreate, Producto, ProductoUpdate

def get_producto(db: Session, producto_id: int) -> Optional[ProductoDB]:
    """Obtiene un producto por su ID"""
    return db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()


def get_productos_disponibles(db: Session, skip: int = 0, limit: int = 100) -> List[ProductoDB]:
    """Obtiene todos los productos disponibles"""
    return (db.query(ProductoDB)
             .filter(ProductoDB.disponible == True)
             .offset(skip)
             .limit(limit)
             .all())

def get_productos_by_menu(db: Session, menu_id: int, skip: int = 0, limit: int = 100, 
                         solo_disponibles: bool = True) -> List[ProductoDB]:
    """Obtiene productos por menú, opcionalmente solo los disponibles"""
    query = db.query(ProductoDB).filter(ProductoDB.id_menu == menu_id)
    
    if solo_disponibles:
        query = query.filter(ProductoDB.disponible == True)
        
    return query.offset(skip).limit(limit).all()

def create_producto(db: Session, producto: ProductoCreate) -> ProductoDB:
    """Crea un nuevo producto"""
    db_producto = ProductoDB(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto_data: dict) -> Optional[ProductoDB]:
    """Actualiza un producto"""
    db_producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if not db_producto:
        return None
    
    # Actualizar campos
    for key, value in producto_data.items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int) -> bool:
    """Elimina un producto si no tiene pedidos asociados"""
    from sqlalchemy import exists, and_
    
    # Verificar si el producto tiene pedidos
    try:
        tiene_pedidos = db.query(
            exists().where(
                models.PedidoItemDB.id_producto == producto_id
            )
        ).scalar()
        
        if tiene_pedidos:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar un producto con pedidos asociados"
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        # Si hay algún error al verificar, asumimos que no hay pedidos
        pass
    
    db_producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if not db_producto:
        return False
    
    db.delete(db_producto)
    db.commit()
    return True
