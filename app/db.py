from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from .core.config import settings

# Crear motor de base de datos
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
    echo=settings.SQL_ECHO  # Mostrar consultas SQL en consola
)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db() -> Session:
    """
    Obtiene una nueva sesión de base de datos.
    La sesión debe ser cerrada manualmente por el llamador.
    """
    return SessionLocal()

def create_tables():
    """
    Crea todas las tablas definidas en los modelos.
    Solo para desarrollo/pruebas.
    """
    from .models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")