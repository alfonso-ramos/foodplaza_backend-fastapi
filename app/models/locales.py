from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import Base
from .usuarios import TipoUsuario

class LocalDB(Base):
    __tablename__ = "locales"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    descripcion = Column(String(500))
    direccion = Column(String(200), nullable=False)
    horario_apertura = Column(String(5), nullable=False)  # Formato HH:MM
    horario_cierre = Column(String(5), nullable=False)    # Formato HH:MM
    tipo_comercio = Column(String(50), nullable=False)
    id_gerente = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    estado = Column(String(20), default='activo', nullable=False)
    plaza_id = Column(Integer, ForeignKey('plazas.id'), nullable=False)
    
    # Relaciones
    plaza = relationship("PlazaDB", back_populates="locales")
    gerente = relationship("UsuarioDB", back_populates="locales")
    productos = relationship("ProductoDB", back_populates="local", cascade="all, delete-orphan")
    menus = relationship("MenuDB", back_populates="local", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<LocalDB(id={self.id}, nombre='{self.nombre}', plaza_id={self.plaza_id})>"

# Nota: Los modelos PlazaDB y ProductoDB deben estar definidos en sus respectivos archivos
