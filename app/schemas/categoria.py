from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


#Modelo base para categoria
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


#Crear una nueva categoria
class CategoriaCreate(CategoriaBase):
    id_tienda: int
    pass


#Actualizar categoria
class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


#Respuesta de categoria
class CategoriaResponse(CategoriaBase):
    id_categoria: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
