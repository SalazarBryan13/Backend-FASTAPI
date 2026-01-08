from pydantic import BaseModel, Field
from typing import Optional

from supabase_auth import datetime

class InventarioBase(BaseModel):
    id_tienda:int
    stock:int=0
    descripcion:Optional[str]= None

class InventarioCreate(InventarioBase):
    pass
class InventarioUpdate(BaseModel):
    stock:Optional[int]=None
    descripcion:Optional[str]= None

class InventarioResponse(InventarioBase):
    id_inventario:int
    fecha_actualizacion:Optional[datetime]= None
    created_at:datetime
    updated_at:datetime


    class Config:
        from_attributes = True