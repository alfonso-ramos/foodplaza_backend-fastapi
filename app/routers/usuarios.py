from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from .. import models, schemas
from ..db import get_db
from ..crud import usuarios as crud_usuarios
from ..services.cloudinary_service import upload_image, delete_image

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

@router.post("/{usuario_id}/imagen", response_model=schemas.ImagenResponse)
async def subir_imagen_perfil(
    usuario_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Sube una imagen de perfil para el usuario especificado.
    
    - **usuario_id**: ID del usuario
    - **file**: Archivo de imagen a subir (jpg, jpeg, png, webp)
    """
    # Verificar que el usuario existe
    db_usuario = crud_usuarios.get_usuario(db, usuario_id=usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar tipo de archivo
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de archivo no permitido. Tipos permitidos: {', '.join(allowed_types)}"
        )
    
    try:
        # Leer el contenido del archivo
        file_content = await file.read()
        
        # Subir a Cloudinary
        upload_result = upload_image(
            file_content,
            folder="usuarios",
            public_id=f"user_{usuario_id}"
        )
        
        # Actualizar usuario con la nueva imagen
        if db_usuario.imagen_public_id:
            delete_image(db_usuario.imagen_public_id)
        
        db_usuario.imagen_url = upload_result["url"]
        db_usuario.imagen_public_id = upload_result["public_id"]
        db.commit()
        db.refresh(db_usuario)
        
        return {
            "url": upload_result["url"],
            "public_id": upload_result["public_id"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al subir la imagen: {str(e)}"
        )

@router.post("/login", response_model=dict)
async def login(credenciales: models.UsuarioLogin, db: Session = Depends(get_db)):
    """Inicia sesión con email y contraseña"""
    try:
        usuario = crud_usuarios.authenticate_user(
            db, 
            email=credenciales.email, 
            password=credenciales.password
        )
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        # Respuesta simple sin JWT
        return {
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "rol": usuario.rol,
                "estado": usuario.estado
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en el servidor: {str(e)}"
        )
