from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    precio: float = Field(..., gt=0, description="El precio debe ser mayor que cero")
    disponible: bool = Field(default=True)
    imagen_url: Optional[str] = Field(None, max_length=255)
    menu_id: int = Field(..., gt=0, description="ID del menú al que pertenece el producto")
    local_id: int = Field(..., gt=0, description="ID del local al que pertenece el producto")

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    precio: Optional[float] = Field(None, gt=0, description="El precio debe ser mayor que cero")
    disponible: Optional[bool] = None
    imagen_url: Optional[str] = Field(None, max_length=255)

class ProductoInDBBase(ProductoBase):
    id: int
    
    model_config = ConfigDict(
        from_attributes=True  # Replaces orm_mode in Pydantic v2
    )

class Producto(ProductoInDBBase):
    pass
