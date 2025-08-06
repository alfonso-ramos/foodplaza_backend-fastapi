import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# Crear motor de base de datos
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Importar modelos para asegurar que se registren con SQLAlchemy
from app.models import ResetCodeDB  # noqa

def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def create_tables():
    """Crear tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)