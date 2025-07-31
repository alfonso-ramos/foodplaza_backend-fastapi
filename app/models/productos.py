from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base

class ProductoDB(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    descripcion = Column(Text)
    precio = Column(Float, nullable=False)
    disponible = Column(Boolean, default=True)
    imagen_url = Column(String(255))
    menu_id = Column(Integer, ForeignKey('menus.id'), nullable=False)
    local_id = Column(Integer, ForeignKey('locales.id'), nullable=False)
    
    # Relaciones
    menu = relationship("MenuDB", back_populates="productos")
    local = relationship("LocalDB", back_populates="productos")
    
    def __repr__(self):
        return f"<ProductoDB(id={self.id}, nombre='{self.nombre}', menu_id={self.menu_id})>"
