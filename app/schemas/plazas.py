from pydantic import ConfigDict, Field
from pydantic import BaseModel
from typing import Optional

class PlazaBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    direccion: str = Field(..., max_length=200)
    estado: str = Field('activo', max_length=20)

class PlazaCreate(PlazaBase):
    pass

class Plaza(PlazaBase):
    id: int
    
    model_config = ConfigDict(
        from_attributes=True  # Replaces orm_mode in Pydantic v2
    )

class PlazaUpdate(BaseModel):
    """
    Esquema para actualizar una plaza. Todos los campos son opcionales.
    """
    nombre: Optional[str] = Field(None, max_length=100)
    direccion: Optional[str] = Field(None, max_length=200)
    estado: Optional[str] = Field(None, max_length=20)
    
    model_config = ConfigDict(
        from_attributes=True
    )
