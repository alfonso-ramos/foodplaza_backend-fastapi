from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..db import get_db
from ..crud import usuarios as crud_usuarios

router = APIRouter()

@router.post("/", response_model=models.Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: models.UsuarioCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario"""
    db_usuario = crud_usuarios.get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está registrado"
        )
    return crud_usuarios.create_usuario(db=db, usuario_data=usuario)

@router.get("/", response_model=List[models.Usuario])
def leer_usuarios(
    skip: int = 0, 
    limit: int = 100,
    estado: str = None,
    db: Session = Depends(get_db)
):
    """Obtiene la lista de usuarios con paginación"""
    if estado and estado not in ["activo", "inactivo"]:
        raise HTTPException(
            status_code=400,
            detail="El estado debe ser 'activo' o 'inactivo'"
        )
    return crud_usuarios.get_usuarios(db, skip=skip, limit=limit, estado=estado)

@router.get("/{usuario_id}", response_model=models.Usuario)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario por su ID"""
    db_usuario = crud_usuarios.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.put("/{usuario_id}", response_model=models.Usuario)
def actualizar_usuario(
    usuario_id: int, 
    usuario: models.UsuarioUpdate, 
    db: Session = Depends(get_db)
):
    """Actualiza un usuario existente"""
    db_usuario = crud_usuarios.update_usuario(db, usuario_id=usuario_id, usuario_data=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario (cambia su estado a inactivo)"""
    if not crud_usuarios.delete_usuario(db, usuario_id=usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None

@router.post("/login")
def login(credenciales: models.UsuarioLogin, db: Session = Depends(get_db)):
    """Inicia sesión con email y contraseña"""
    usuario = crud_usuarios.authenticate_user(
        db, 
        email=credenciales.email, 
        password=credenciales.password
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # En una implementación futura, aquí se generaría un token JWT
    return {
        "mensaje": "Inicio de sesión exitoso",
        "usuario_id": usuario.id,
        "nombre": usuario.nombre,
        "rol": usuario.rol
    }
