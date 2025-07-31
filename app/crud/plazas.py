from sqlalchemy.orm import Session
from ..models import PlazaDB
from ..schemas.plazas import PlazaCreate
from typing import Dict, Any, Optional

def get_plaza(db: Session, plaza_id: int):
    return db.query(PlazaDB).filter(PlazaDB.id == plaza_id).first()

def get_plazas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PlazaDB).offset(skip).limit(limit).all()

def create_plaza(db: Session, plaza: PlazaCreate) -> PlazaDB:
    """
    Crea una nueva plaza en la base de datos.
    
    Args:
        db: Sesión de base de datos
        plaza: Datos de la plaza a crear
        
    Returns:
        PlazaDB: La plaza creada
        
    Raises:
        ValueError: Si hay un error de validación
    """
    # Convertir el modelo Pydantic a diccionario
    plaza_data = plaza.dict()
    
    # Verificar si ya existe una plaza con el mismo nombre
    existing_plaza = db.query(PlazaDB).filter(
        PlazaDB.nombre == plaza_data["nombre"]
    ).first()
    
    if existing_plaza:
        raise ValueError(f"Ya existe una plaza con el nombre: {plaza_data['nombre']}")
    
    try:
        # Crear la nueva plaza
        db_plaza = PlazaDB(**plaza_data)
        db.add(db_plaza)
        db.commit()
        db.refresh(db_plaza)
        return db_plaza
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error al crear la plaza: {str(e)}")

def update_plaza(db: Session, plaza_id: int, plaza_data: Dict[str, Any]) -> Optional[PlazaDB]:
    """
    Actualiza una plaza existente.
    
    Args:
        db: Sesión de base de datos
        plaza_id: ID de la plaza a actualizar
        plaza_data: Diccionario con los campos a actualizar
        
    Returns:
        Optional[PlazaDB]: La plaza actualizada o None si no se encontró
    """
    db_plaza = db.query(PlazaDB).filter(PlazaDB.id == plaza_id).first()
    if not db_plaza:
        return None
    
    for key, value in plaza_data.items():
        setattr(db_plaza, key, value)
    
    db.add(db_plaza)
    db.commit()
    db.refresh(db_plaza)
    return db_plaza

def delete_plaza(db: Session, plaza_id: int) -> bool:
    """
    Elimina una plaza de la base de datos.
    
    Args:
        db: Sesión de base de datos
        plaza_id: ID de la plaza a eliminar
        
    Returns:
        bool: True si se eliminó correctamente, False si no se encontró la plaza
    """
    db_plaza = db.query(PlazaDB).filter(PlazaDB.id == plaza_id).first()
    if not db_plaza:
        return False
    
    db.delete(db_plaza)
    db.commit()
    return True
