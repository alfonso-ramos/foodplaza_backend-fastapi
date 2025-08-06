from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, condecimal

class PedidoItemBase(BaseModel):
    id_producto: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: condecimal(gt=0, decimal_places=2)
    instrucciones_especiales: Optional[str] = None

class PedidoItemCreate(PedidoItemBase):
    pass

class PedidoItemUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, gt=0)
    instrucciones_especiales: Optional[str] = None

class PedidoItem(PedidoItemBase):
    id: int
    id_pedido: int

    class Config:
        from_attributes = True

class PedidoBase(BaseModel):
    id_local: int
    instrucciones_especiales: Optional[str] = None

class PedidoCreate(PedidoBase):
    items: List[PedidoItemCreate]

class PedidoUpdate(BaseModel):
    estado_pedido: Optional[str] = None
    instrucciones_especiales: Optional[str] = None
    tiempo_preparacion_estimado: Optional[int] = None

class Pedido(PedidoBase):
    id: int
    id_usuario: int
    fecha_pedido: datetime
    estado_pedido: str
    total_pedido: condecimal(gt=0, decimal_places=2)
    tiempo_preparacion_estimado: int
    items: List[PedidoItem] = []

    class Config:
        from_attributes = True
