from pydantic import ConfigDict, Field, field_validator
from pydantic import BaseModel
from typing import Optional, Any

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
    
    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode in Pydantic v2
        extra='ignore'
    )
