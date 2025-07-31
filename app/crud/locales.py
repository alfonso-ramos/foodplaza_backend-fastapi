from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models import LocalDB, UsuarioDB

def get_locale(db: Session, locale_id: int):
    return db.query(LocalDB).filter(LocalDB.id == locale_id).first()

def get_locales(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    plaza_id: int = None,
    tipo_comercio: str = None,
    id_gerente: int = None
):
    query = db.query(LocalDB)
    
    # Aplicar filtros si se proporcionan
    if plaza_id is not None:
        query = query.filter(LocalDB.plaza_id == plaza_id)
    if tipo_comercio is not None:
        query = query.filter(LocalDB.tipo_comercio == tipo_comercio.lower())
    if id_gerente is not None:
        query = query.join(UsuarioDB, LocalDB.id_gerente == UsuarioDB.id)
        query = query.filter(UsuarioDB.id == id_gerente)
    
    return query.offset(skip).limit(limit).all()

def create_locale(db: Session, locale):
    # Verificar que el gerente exista y sea un gerente si se proporciona
    if locale.id_gerente is not None:
        gerente = db.query(UsuarioDB).filter(
            UsuarioDB.id == locale.id_gerente,
            UsuarioDB.rol == 'gerente',
            UsuarioDB.estado == 'activo'
        ).first()
        if not gerente:
            raise ValueError("El ID de gerente proporcionado no es válido o el usuario no tiene permisos de gerente")
    
    # Convertir el tipo de comercio a minúsculas
    locale_data = locale.dict()
    if 'tipo_comercio' in locale_data and locale_data['tipo_comercio']:
        locale_data['tipo_comercio'] = locale_data['tipo_comercio'].lower()
    
    db_locale = LocalDB(**locale_data)
    db.add(db_locale)
    db.commit()
    db.refresh(db_locale)
    return db_locale

def update_locale(db: Session, locale_id: int, locale_data):
    db_locale = db.query(LocaleDB).filter(LocaleDB.id == locale_id).first()
    if not db_locale:
        return None
    
    update_data = locale_data.dict(exclude_unset=True)
    
    # Verificar que el nuevo gerente exista y sea un gerente si se está actualizando
    if 'id_gerente' in update_data and update_data['id_gerente'] is not None:
        gerente = db.query(UsuarioDB).filter(
            UsuarioDB.id == update_data['id_gerente'],
            UsuarioDB.rol == 'gerente',
            UsuarioDB.estado == 'activo'
        ).first()
        if not gerente:
            raise ValueError("El ID de gerente proporcionado no es válido o el usuario no tiene permisos de gerente")
    
    # Convertir el tipo de comercio a minúsculas si se está actualizando
    if 'tipo_comercio' in update_data and update_data['tipo_comercio']:
        update_data['tipo_comercio'] = update_data['tipo_comercio'].lower()
    
    # Actualizar campos
    for key, value in update_data.items():
        setattr(db_locale, key, value)
    
    db.commit()
    db.refresh(db_locale)
    return db_locale

def delete_locale(db: Session, locale_id: int):
    db_locale = db.query(LocaleDB).filter(LocaleDB.id == locale_id).first()
    if not db_locale:
        return False
    
    db.delete(db_locale)
    db.commit()
    return True