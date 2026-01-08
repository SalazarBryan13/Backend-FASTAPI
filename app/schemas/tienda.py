from pydantic import BaseModel, Field
from typing import Optional


#Modelo base para la tienda no se pone el id porque es autogenerado
class TiendaBase(BaseModel):
    id_propietario:str
    nombre_tienda:str
    descripcion:Optional[str] = None
    telefono:Optional[str]= None
    direccion:Optional[str]= None
    estado:str
    imagen_url :Optional[str]= None

#Herencia para crear una nueva tienda
class TiendaCreate(TiendaBase):
    pass

#Actualizar tienda
class TiendaUpdate(BaseModel):
    nombre_tienda:Optional[str]= None
    descripcion:Optional[str] = None
    telefono:Optional[str]= None
    direccion:Optional[str]= None
    estado:Optional[str]= None
    imagen_url :Optional[str]= None

class TiendasResponse(TiendaBase):
    id_tienda:int

    class Config:
        from_attributes = True