from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Float
from sqlalchemy.orm import relationship
from .base import Base

class MenuDB(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    descripcion = Column(Text)
    precio = Column(Float, nullable=False)
    disponible = Column(Boolean, default=True)
    imagen_url = Column(String(255))
    local_id = Column(Integer, ForeignKey('locales.id'), nullable=False)
    
    # Relaciones
    local = relationship("LocalDB", back_populates="menus")
    productos = relationship("ProductoDB", back_populates="menu", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MenuDB(id={self.id}, nombre='{self.nombre}', local_id={self.local_id})>"
