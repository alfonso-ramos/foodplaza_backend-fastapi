from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models
from ..schemas import imagenes as schemas

def get_imagen(db: Session, imagen_id: int) -> Optional[models.ImagenDB]:
    """Obtiene una imagen por su ID."""
    return db.query(models.ImagenDB).filter(models.ImagenDB.id == imagen_id).first()

def get_imagenes_entidad(
    db: Session, 
    tipo_entidad: str, 
    entidad_id: int,
    skip: int = 0, 
    limit: int = 100
) -> List[models.ImagenDB]:
    """Obtiene todas las imágenes de una entidad específica."""
    return (
        db.query(models.ImagenDB)
        .filter(
            models.ImagenDB.tipo_entidad == tipo_entidad,
            models.ImagenDB.entidad_id == entidad_id
        )
        .order_by(models.ImagenDB.orden, models.ImagenDB.fecha_subida)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_imagen_principal(
    db: Session, 
    tipo_entidad: str, 
    entidad_id: int
) -> Optional[models.ImagenDB]:
    """Obtiene la imagen principal de una entidad, si existe."""
    return (
        db.query(models.ImagenDB)
        .filter(
            models.ImagenDB.tipo_entidad == tipo_entidad,
            models.ImagenDB.entidad_id == entidad_id,
            models.ImagenDB.es_principal == True
        )
        .first()
    )

def create_imagen(
    db: Session, 
    imagen: schemas.ImagenCreate,
    url: str
) -> models.ImagenDB:
    """Crea una nueva imagen para una entidad."""
    # Si se marca como principal, desmarcar cualquier otra imagen principal
    if imagen.es_principal:
        db.query(models.ImagenDB).filter(
            models.ImagenDB.tipo_entidad == imagen.tipo_entidad,
            models.ImagenDB.entidad_id == imagen.entidad_id,
            models.ImagenDB.es_principal == True
        ).update({"es_principal": False})
    
    db_imagen = models.ImagenDB(
        url=url,
        tipo_entidad=imagen.tipo_entidad,
        entidad_id=imagen.entidad_id,
        es_principal=imagen.es_principal,
        orden=imagen.orden,
        metadata_=imagen.metadata
    )
    
    db.add(db_imagen)
    db.commit()
    db.refresh(db_imagen)
    return db_imagen

def update_imagen(
    db: Session, 
    db_imagen: models.ImagenDB,
    imagen: schemas.ImagenUpdate
) -> models.ImagenDB:
    """Actualiza los metadatos de una imagen existente."""
    update_data = imagen.dict(exclude_unset=True)
    
    # Manejar el campo metadata_ (que en la base de datos es metadata_ pero en el esquema es metadata)
    if 'metadata' in update_data:
        update_data['metadata_'] = update_data.pop('metadata')
    
    # Si se está marcando como principal, desmarcar cualquier otra imagen principal
    if update_data.get('es_principal', False):
        db.query(models.ImagenDB).filter(
            models.ImagenDB.tipo_entidad == db_imagen.tipo_entidad,
            models.ImagenDB.entidad_id == db_imagen.entidad_id,
            models.ImagenDB.es_principal == True,
            models.ImagenDB.id != db_imagen.id
        ).update({"es_principal": False})
    
    for field, value in update_data.items():
        setattr(db_imagen, field, value)
    
    db.commit()
    db.refresh(db_imagen)
    return db_imagen

def delete_imagen(db: Session, db_imagen: models.ImagenDB) -> bool:
    """Elimina una imagen de la base de datos."""
    db.delete(db_imagen)
    db.commit()
    return True

def get_imagenes_count(
    db: Session, 
    tipo_entidad: str, 
    entidad_id: int
) -> int:
    """Obtiene el número total de imágenes para una entidad."""
    return (
        db.query(models.ImagenDB)
        .filter(
            models.ImagenDB.tipo_entidad == tipo_entidad,
            models.ImagenDB.entidad_id == entidad_id
        )
        .count()
    )
