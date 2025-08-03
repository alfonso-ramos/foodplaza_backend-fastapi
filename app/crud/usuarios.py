from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
from datetime import datetime
from ..models import UsuarioDB

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_usuario(db: Session, usuario_id: int):
    """Obtiene un usuario por su ID"""
    return db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    """Obtiene un usuario por su email"""
    print(f"[DEBUG] Buscando usuario con email: {email}")
    try:
        # Primero intentamos con búsqueda exacta
        usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
        
        # Si no encontramos, intentamos con case-insensitive
        if not usuario:
            print(f"[DEBUG] Búsqueda exacta fallida, intentando case-insensitive")
            usuario = db.query(UsuarioDB).filter(
                func.lower(UsuarioDB.email) == func.lower(email)
            ).first()
        
        if usuario:
            print(f"[DEBUG] Usuario encontrado: ID={usuario.id}, Email={usuario.email}")
        else:
            print(f"[DEBUG] No se encontró usuario con email: {email}")
            
        return usuario
    except Exception as e:
        print(f"[ERROR] Error al buscar usuario por email {email}: {str(e)}")
        return None

def get_usuarios(db: Session, skip: int = 0, limit: int = 100, estado: str = None):
    """Lista usuarios con paginación y filtro opcional por estado"""
    query = db.query(UsuarioDB)
    if estado:
        query = query.filter(UsuarioDB.estado == estado)
    return query.offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario_data):
    """Crea un nuevo usuario con la contraseña hasheada"""
    # Convertir el modelo a diccionario
    usuario_dict = usuario_data.dict()
    # Hashear la contraseña
    hashed_password = pwd_context.hash(usuario_dict["password"])
    # Crear el usuario en la base de datos
    db_usuario = UsuarioDB(
        **{k: v for k, v in usuario_dict.items() if k != 'password'},
        password=hashed_password
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario_data):
    """Actualiza un usuario existente"""
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        return None
    
    # Convertir el modelo a diccionario excluyendo los campos no establecidos
    update_data = usuario_data.dict(exclude_unset=True)
    
    # Si se proporciona una nueva contraseña, hashearla
    if "password" in update_data:
        update_data["password"] = pwd_context.hash(update_data["password"])
    
    # Actualizar los campos del usuario
    for key, value in update_data.items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    """Elimina un usuario (cambia su estado a inactivo)"""
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        return False
    
    db_usuario.estado = "inactivo"
    db.commit()
    db.refresh(db_usuario)
    return True

def authenticate_user(db: Session, email: str, password: str):
    """Autentica un usuario por email y contraseña"""
    user = get_usuario_by_email(db, email)
    if not user:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user
