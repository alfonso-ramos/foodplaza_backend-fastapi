from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from typing import Optional
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
