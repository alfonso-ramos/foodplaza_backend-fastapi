from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class PlazaDB(Base):
    __tablename__ = "plazas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    direccion = Column(String(200), nullable=False)
    estado = Column(String(20), default='activo', nullable=False)
    
    # Relaciones
    locales = relationship("LocalDB", back_populates="plaza", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PlazaDB(id={self.id}, nombre='{self.nombre}')>"
