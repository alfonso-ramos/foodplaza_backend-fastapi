
import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración general de la aplicación
    PROJECT_NAME: str = "FoodPlaza API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # Configuración de base de datos
    DB_DRIVER: str = "mysql+pymysql"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "foodplaza"
    
    # Configuración de SQLAlchemy
    SQL_ECHO: bool = False
    POOL_RECYCLE: int = 3600
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 20
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Cargar configuración
settings = Settings()

# Mostrar configuración en modo debug
if settings.DEBUG:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Configuración cargada:")
    for key, value in settings.dict().items():
        if "PASSWORD" in key and value:
            value = "*****"
        logger.info(f"  {key}: {value}")
