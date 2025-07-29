from sqlalchemy.orm import Session
from ..models import ProductoDB, ProductoCreate, Producto, ProductoUpdate

def get_producto(db: Session, producto_id: int):
    return db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()

def get_productos_by_menu(db: Session, menu_id: int, skip: int = 0, limit: int = 100, disponible: bool = None):
    query = db.query(ProductoDB).filter(ProductoDB.id_menu == menu_id)
    
    if disponible is not None:
        query = query.filter(ProductoDB.disponible == disponible)
        
    return query.offset(skip).limit(limit).all()

def create_producto(db: Session, producto: ProductoCreate):
    db_producto = ProductoDB(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto_data: dict):
    db_producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if not db_producto:
        return None
    
    for key, value in producto_data.items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int):
    db_producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if not db_producto:
        return False
    
    db.delete(db_producto)
    db.commit()
    return True
