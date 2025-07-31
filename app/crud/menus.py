from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.menus import MenuDB
from ..schemas.menus import MenuCreate, MenuUpdate

def get_menu(db: Session, menu_id: int):
    """Obtiene un menú por su ID"""
    return db.query(MenuDB).filter(MenuDB.id == menu_id).first()

def get_menus_by_local(
    db: Session, 
    local_id: int, 
    skip: int = 0, 
    limit: int = 100,
    nombre: str = None,
    disponible: bool = None
):
    """Obtiene todos los menús de un local con opciones de filtrado"""
    query = db.query(MenuDB).filter(MenuDB.local_id == local_id)
    
    if nombre:
        query = query.filter(MenuDB.nombre.ilike(f"%{nombre}%"))
    
    if disponible is not None:
        query = query.filter(MenuDB.disponible == disponible)
    
    return query.offset(skip).limit(limit).all()

def create_menu(db: Session, menu: MenuCreate):
    """Crea un nuevo menú"""
    db_menu = MenuDB(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def update_menu(db: Session, menu_id: int, menu_data: MenuUpdate):
    """Actualiza un menú existente"""
    db_menu = get_menu(db, menu_id=menu_id)
    if not db_menu:
        return None
    
    update_data = menu_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_menu, key, value)
    
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def delete_menu(db: Session, menu_id: int):
    """Elimina un menú"""
    db_menu = get_menu(db, menu_id=menu_id)
    if not db_menu:
        return False
    
    db.delete(db_menu)
    db.commit()
    return True
