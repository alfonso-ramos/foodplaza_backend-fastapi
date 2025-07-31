from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.usuarios import UsuarioDB

def get_current_user(db: Session = Depends(get_db)) -> UsuarioDB:
    # Simulate a logged-in user for development purposes
    user = db.query(UsuarioDB).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No users in the database. Please create a user first.",
        )
    return user

def get_current_active_user(current_user: UsuarioDB = Depends(get_current_user)) -> UsuarioDB:
    if current_user.estado != "activo":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user