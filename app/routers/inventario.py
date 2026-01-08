from fastapi import APIRouter,HTTPException,Depends
from typing import Annotated, Any, Dict, List
from fastapi import Depends, HTTPException, Path, Query
from ..database import get_supabase
from ..schemas.inventario import InventarioCreate, InventarioUpdate, InventarioResponse
from supabase import Client
from ..dependencies import get_current_user_id,get_current_tienda_id

router = APIRouter(prefix="/inventarios", tags=["inventarios"])

def get_db() -> Client:
    return get_supabase()
DbDependency = Annotated[Client, Depends(get_db)]

#obtener todos los inventarios
@router.get("/",response_model=List[InventarioResponse])
def get_inventarios(db: DbDependency):
    inventarios = db.table("inventario").select("*").execute()
    return inventarios.data


#obtener inventario por id_tienda
@router.get("/{id_tienda}",response_model=List[InventarioResponse])
def get_inventario_por_tienda(db:DbDependency,id_tienda:int):
    inventarios=db.table("inventario").select("*").eq("id_tienda",id_tienda).execute()
    return inventarios.data


@router.put("/{id_inventario}",response_model= InventarioResponse,status_code=200)
def actualizar_inventario(db:DbDependency,id_inventario:int,tienda_update:InventarioUpdate):
    datos=tienda_update.model_dump(exclude_unset=True)
    inventario_actualizado=db.table("inventario").update(datos).eq("id_inventario",id_inventario).execute()
    if not inventario_actualizado.data:
        raise HTTPException(status_code=400,detail="Error al actualizar el inventario")
    return inventario_actualizado.data[0]

@router.post("/",response_model=InventarioResponse,status_code=201)
def crear_inventario(db:DbDependency,inventario:InventarioCreate):
    nuevo_inventario=db.table("inventario").insert(inventario.model_dump()).execute()
    if not nuevo_inventario.data:
        raise HTTPException(status_code=400,detail="Error al crear el inventario")
    return nuevo_inventario.data[0]

@router.delete("/{id_inventario}",status_code=204)
def eliminar_inventario(db:DbDependency,id_inventario:int):
    response=db.table("inventario").delete().eq("id_inventario",id_inventario).execute()
    if not response.data:
        raise HTTPException(status_code=400,detail="Error al eliminar el inventario")
    return None