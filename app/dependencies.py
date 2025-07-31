from typing import Generator
from sqlalchemy.orm import Session
from .db import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Obtiene una sesión de base de datos para la solicitud actual.
    La sesión se cierra automáticamente al finalizar la solicitud.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Re-exportar tipos y configuraciones útiles
__all__ = ["get_db"]
