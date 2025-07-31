from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from .base import Base

class ImagenDB(Base):
    __tablename__ = 'imagenes'
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    tipo_entidad = Column(String(20), nullable=False)  # 'plaza', 'local', 'producto', 'usuario'
    entidad_id = Column(Integer, nullable=False)
    es_principal = Column(Boolean, default=False)
    orden = Column(Integer, default=0)
    fecha_subida = Column(DateTime(timezone=True), server_default=func.now())
    metadata_ = Column('metadata', JSON, nullable=True)
    
    __table_args__ = (
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci'
        }
    )
    
    def __repr__(self):
        return f"<Imagen(id={self.id}, tipo_entidad='{self.tipo_entidad}', entidad_id={self.entidad_id})>"

# Crear índices para mejorar el rendimiento de consultas comunes
# Se crean en una migración separada para evitar problemas con SQLAlchemy-Alembic
