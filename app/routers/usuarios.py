
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.usuarios import Usuario, UsuarioCreate, UsuarioUpdate
from app.crud import usuarios as crud_usuarios

router = APIRouter()

@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED, summary="Create a new user", description="Create a new user with the provided data.")
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud_usuarios.get_usuario_by_email(db, email=usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_usuarios.create_usuario(db=db, usuario=usuario)

@router.get("/", response_model=List[Usuario], summary="Get all users", description="Get a list of all users.")
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_usuarios.get_usuarios(db, skip=skip, limit=limit)
    return users

@router.get("/{usuario_id}", response_model=Usuario, summary="Get a user by ID", description="Get a single user by their ID.")
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_user = crud_usuarios.get_usuario(db, usuario_id=usuario_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{usuario_id}", response_model=Usuario, summary="Update a user", description="Update an existing user's data.")
def update_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_user = crud_usuarios.update_usuario(db, usuario_id=usuario_id, usuario=usuario)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user", description="Delete a user by their ID.")
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    if not crud_usuarios.delete_usuario(db, usuario_id=usuario_id):
        raise HTTPException(status_code=404, detail="User not found")
    return
