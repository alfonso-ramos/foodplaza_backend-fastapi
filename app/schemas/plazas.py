from pydantic import BaseModel, Field
from typing import Optional

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
