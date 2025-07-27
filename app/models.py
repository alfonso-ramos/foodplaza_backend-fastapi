from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from .db import Base

# Modelo de la base de datos
class PlazaDB(Base):
    __tablename__ = 'plazas'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    estado = Column(String(20), default='activo')

# Modelos Pydantic para validación
from pydantic import BaseModel

class PlazaBase(BaseModel):
    nombre: str
    direccion: str
    estado: str = 'activo'

class PlazaCreate(PlazaBase):
    pass

class Plaza(PlazaBase):
    id: int
    
    class Config:
        orm_mode = True
