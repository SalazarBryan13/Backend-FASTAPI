from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


#Modelo base para producto
class ProductoBase(BaseModel):
    id_inventario: int
    id_categoria: int
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal = Field(..., ge=0)
    imagen_url: Optional[str] = None
    activo: bool = True


#Crear un nuevo producto
class ProductoCreate(ProductoBase):
    id_tienda: int
    pass


#Actualizar producto
class ProductoUpdate(BaseModel):
    id_inventario: Optional[int] = None
    id_categoria: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = Field(None, ge=0)
    imagen_url: Optional[str] = None
    activo: Optional[bool] = None


#Respuesta de producto
class ProductoResponse(ProductoBase):
    id_producto: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
