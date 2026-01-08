from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

# Estados válidos para el pedido
EstadoPedido = Literal['pendiente', 'confirmado', 'en_preparacion', 'en_camino', 'entregado', 'cancelado']

# Modelo base para pedido
class PedidoBase(BaseModel):
    id_tienda: int
    id_direccion: int
    estado: EstadoPedido = 'pendiente'
    total: float = Field(default=0, ge=0)
    observaciones: Optional[str] = Field(default=None, max_length=500)

# Para crear un nuevo pedido
class PedidoCreate(BaseModel):
    id_tienda: int
    id_direccion: int
    total: float = Field(default=0, ge=0)
    observaciones: Optional[str] = Field(default=None, max_length=500)

# Para actualizar solo el estado del pedido
class PedidoUpdateEstado(BaseModel):
    estado: EstadoPedido

# Respuesta completa del pedido
class PedidoResponse(PedidoBase):
    id_pedido: int
    fecha_pedido: Optional[datetime] = None
    fecha_confirmacion: Optional[datetime] = None
    fecha_entrega: Optional[datetime] = None

    class Config:
        from_attributes = True
