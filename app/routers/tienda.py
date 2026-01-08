from fastapi import APIRouter,HTTPException,Depends
from typing import Annotated, Any, Dict, List
from fastapi import Depends, HTTPException, Path, Query
from ..database import get_supabase
from ..schemas.tienda import TiendaCreate, TiendaUpdate, TiendasResponse, TiendaBase
from supabase import Client
from ..dependencies import get_current_user_id,get_current_tienda_id

router = APIRouter(prefix="/tiendas", tags=["tiendas"])

def get_db() -> Client:
    return get_supabase()

DbDependency = Annotated[Client, Depends(get_db)]

#obtener todas las tiendas
@router.get("/",response_model=List[TiendasResponse])
def get_tiendas(db: DbDependency, id_user: str = Depends(get_current_user_id)):
    tiendas = db.table("tienda").select("*").eq("id_propietario", id_user).execute()
    return tiendas.data
    


#crear tiendas
@router.post("/",response_model=TiendasResponse ,status_code=201)
def crear_tienda(tienda:TiendaCreate,db:DbDependency):
    nueva_tienda= db.table("tienda").insert(tienda.model_dump()).execute()
    if not nueva_tienda.data:
        raise HTTPException(status_code=400,detail="Error al crear la tienda")
    return nueva_tienda.data[0]


#actualizar tiendas

@router.put("/{id_tienda}",response_model=TiendasResponse,status_code=200)
def actualizar_tienda(id_tienda:int,tienda_update:TiendaUpdate,db:DbDependency,user_id:str=Depends(get_current_user_id)):
    dato = tienda_update.model_dump(exclude_unset=True)
    tienda_actualizada = db.table("tienda").update(dato).eq("id_tienda",id_tienda).eq("id_propietario",user_id).execute()
    if not tienda_actualizada.data:
        raise HTTPException(status_code=400,detail="Error al actualizar la tienda")
    return tienda_actualizada.data[0]


#eliminar tienda
@router.delete("/{id_tienda}",status_code=204)
def eliminar_tienda(id_tienda:int,db:DbDependency,user_id:str=Depends(get_current_user_id)):
    response = db.table("tienda").delete().eq("id_tienda",id_tienda).eq("id_propietario",user_id).execute()
    if not response.data:
        raise HTTPException(status_code=400,detail="Error al eliminar la tienda")
    return None





