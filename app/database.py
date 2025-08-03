from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost/foodplaza"

# Crear el motor de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=10
)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos
Base = declarative_base()

def get_db():
    """
    Proveedor de dependencia para obtener una sesión de base de datos.
    Se cierra automáticamente después de su uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
