from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.usuarios import UsuarioDB, TipoUsuario
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_usuario(db: Session, usuario_id: int):
    return db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UsuarioDB).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: UsuarioCreate):
    hashed_password = get_password_hash(usuario.password)
    db_usuario = UsuarioDB(
        email=usuario.email,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        hashed_password=hashed_password,
        tipo=usuario.tipo,
        estado=usuario.estado,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        return None
    update_data = usuario.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        return False
    db_usuario.estado = "inactivo"
    db.commit()
    return True

def authenticate_user(db: Session, email: str, password: str):
    user = get_usuario_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user