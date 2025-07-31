from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.productos import ProductoDB
from ..schemas.productos import ProductoCreate, ProductoUpdate

def get_producto(db: Session, producto_id: int):
    """Obtiene un producto por su ID"""
    return db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()

def get_productos_by_menu(
    db: Session, 
    menu_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    disponible: bool = None,
    nombre: str = None
):
    """
    Obtiene los productos de un menú específico con opciones de filtrado.
    """
    query = db.query(ProductoDB).filter(ProductoDB.menu_id == menu_id)
    
    if disponible is not None:
        query = query.filter(ProductoDB.disponible == disponible)
        
    if nombre:
        query = query.filter(ProductoDB.nombre.ilike(f"%{nombre}%"))
        
    return query.offset(skip).limit(limit).all()

def create_producto(db: Session, producto: ProductoCreate):
    """Crea un nuevo producto"""
    db_producto = ProductoDB(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto_data: ProductoUpdate):
    """Actualiza un producto existente"""
    db_producto = get_producto(db, producto_id=producto_id)
    if not db_producto:
        return None
    
    update_data = producto_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producto, key, value)
    
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int):
    """Elimina un producto"""
    db_producto = get_producto(db, producto_id=producto_id)
    if not db_producto:
        return False
    
    db.delete(db_producto)
    db.commit()
    return True
