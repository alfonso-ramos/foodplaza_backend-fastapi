from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class MenuBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    precio: float = Field(..., gt=0, description="El precio debe ser mayor que cero")
    disponible: bool = Field(default=True)
    imagen_url: Optional[str] = Field(None, max_length=255)
    local_id: int = Field(..., gt=0, description="ID del local al que pertenece el menú")

class MenuCreate(MenuBase):
    pass

class MenuUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    precio: Optional[float] = Field(None, gt=0, description="El precio debe ser mayor que cero")
    disponible: Optional[bool] = None
    imagen_url: Optional[str] = Field(None, max_length=255)

class MenuInDBBase(MenuBase):
    id: int
    
    model_config = ConfigDict(
        from_attributes=True  # Replaces orm_mode in Pydantic v2
    )

class Menu(MenuInDBBase):
    pass
