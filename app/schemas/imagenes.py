from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class TipoEntidad(str, Enum):
    PLAZA = "plaza"
    LOCAL = "local"
    PRODUCTO = "producto"
    USUARIO = "usuario"

class ImagenBase(BaseModel):
    tipo_entidad: TipoEntidad
    entidad_id: int = Field(..., gt=0)
    es_principal: bool = False
    orden: int = Field(0, ge=0)
    metadata: Optional[Dict[str, Any]] = None

class ImagenCreate(ImagenBase):
    pass

class ImagenUpdate(BaseModel):
    es_principal: Optional[bool] = None
    orden: Optional[int] = Field(None, ge=0)
    metadata: Optional[Dict[str, Any]] = None

class ImagenInDBBase(ImagenBase):
    id: int
    url: str
    fecha_subida: datetime
    
    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode in Pydantic v2
        extra='ignore'
    )

class Imagen(ImagenInDBBase):
    pass

class ImagenInDB(ImagenInDBBase):
    pass
