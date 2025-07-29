from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, Boolean, Enum, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, condecimal, EmailStr, validator
from typing import Optional, List
from .db import Base

# Modelos SQLAlchemy
class PlazaDB(Base):
    __tablename__ = 'plazas'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    estado = Column(String(20), default='activo')
    
    # Relación con locales
    locales = relationship("LocaleDB", back_populates="plaza", cascade="all, delete-orphan")

class LocaleDB(Base):
    __tablename__ = 'locales'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=True)
    direccion = Column(String(200), nullable=False)
    horario_apertura = Column(String(5), nullable=False)  # Formato: 'HH:MM'
    horario_cierre = Column(String(5), nullable=False)    # Formato: 'HH:MM'
    estado = Column(String(20), default='activo')
    plaza_id = Column(Integer, ForeignKey('plazas.id', ondelete='CASCADE'), nullable=False)
    
    # Relación con plaza
    plaza = relationship("PlazaDB", back_populates="locales")

# Modelos Pydantic
class PlazaBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    direccion: str = Field(..., max_length=200)
    estado: str = Field('activo', max_length=20)

class PlazaCreate(PlazaBase):
    pass

class Plaza(PlazaBase):
    id: int
    
    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2

class LocaleBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: str = Field(None, max_length=500)
    direccion: str = Field(..., max_length=200)
    horario_apertura: str = Field(..., pattern='^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')  # Formato HH:MM
    horario_cierre: str = Field(..., pattern='^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')    # Formato HH:MM
    estado: str = Field('activo', max_length=20)
    plaza_id: int

class LocaleCreate(LocaleBase):
    pass

class Locale(LocaleBase):
    id: int
    
    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2

# Modelos para Menús
class MenuDB(Base):
    __tablename__ = 'menus'
    
    id = Column(Integer, primary_key=True, index=True)
    id_local = Column(Integer, ForeignKey('locales.id', ondelete='CASCADE'), nullable=False)
    nombre_menu = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    
    # Relación con productos
    productos = relationship("ProductoDB", back_populates="menu", cascade="all, delete-orphan")

class ProductoDB(Base):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(DECIMAL(10, 2), nullable=False)
    id_menu = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), nullable=False)
    disponible = Column(Boolean, nullable=False, default=True)
    categoria = Column(String(50), nullable=True)
    
    # Relación con menú
    menu = relationship("MenuDB", back_populates="productos")

# Modelos Pydantic para Menús
class MenuBase(BaseModel):
    nombre_menu: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    id_local: int

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: int
    
    class Config:
        from_attributes = True

# Modelos Pydantic para Productos
class ProductoBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    precio: condecimal(gt=0, decimal_places=2)
    disponible: bool = True
    categoria: Optional[str] = Field(None, max_length=50)
    id_menu: int

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    precio: Optional[condecimal(gt=0, decimal_places=2)] = None
    disponible: Optional[bool] = None
    categoria: Optional[str] = Field(None, max_length=50)
    id_menu: Optional[int] = None

class Producto(ProductoBase):
    id: int
    
    class Config:
        from_attributes = True

# Modelo SQLAlchemy para Usuarios
class UsuarioDB(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)
    password = Column(String(255), nullable=False)
    rol = Column(Enum('usuario', 'gerente', 'administrador', name='roles_usuarios'), 
                nullable=False, default='usuario')
    estado = Column(Enum('activo', 'inactivo', name='estados_usuarios'),
                   nullable=False, default='activo')
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_actualizacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# Modelos Pydantic para Usuarios
class UsuarioBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    rol: str = "usuario"
    
    @validator('telefono')
    def validate_telefono(cls, v):
        if v is not None:
            # Remove any non-digit characters
            v = ''.join(filter(str.isdigit, v))
            # Add +52 prefix if not present and length is 10
            if len(v) == 10:
                v = f"+52{v}"
            elif not v.startswith('+') and len(v) > 10:
                v = f"+{v}"
        return v

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe contener al menos una mayúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    rol: Optional[str] = None
    estado: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

class Usuario(UsuarioBase):
    id: int
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
