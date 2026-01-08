from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated, List
from ..database import get_supabase
from ..schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from supabase import Client
from ..dependencies import get_current_user_id, get_current_tienda_id

router = APIRouter(prefix="/categorias", tags=["categorias"])


def get_db() -> Client:
    return get_supabase()


DbDependency = Annotated[Client, Depends(get_db)]


#obtener todas las categorias por tienda
@router.get("/{id_tienda}", response_model=List[CategoriaResponse])
def get_categorias(db: DbDependency, id_tienda: int):
    categorias = db.table("categoria").select("*").eq("id_tienda", id_tienda).execute()
    return categorias.data
    


#crear categoria
@router.post("/", response_model=CategoriaResponse, status_code=201)
def crear_categoria(db: DbDependency, categoria: CategoriaCreate):
    nueva_categoria = db.table("categoria").insert(categoria.model_dump()).execute()
    if not nueva_categoria.data:
        raise HTTPException(status_code=400, detail="Error al crear la categoria")
    return nueva_categoria.data[0]


#actualizar categoria
@router.put("/{id_categoria}", response_model=CategoriaResponse, status_code=200)
def actualizar_categoria(db: DbDependency, id_categoria: int, categoria_update: CategoriaUpdate):
    datos = categoria_update.model_dump(exclude_unset=True)
    categoria_actualizada = db.table("categoria").update(datos).eq("id_categoria", id_categoria).execute()
    if not categoria_actualizada.data:
        raise HTTPException(status_code=400, detail="Error al actualizar la categoria")
    return categoria_actualizada.data[0]


#eliminar categoria
@router.delete("/{id_categoria}", status_code=204)
def eliminar_categoria(db: DbDependency, id_categoria: int):
    response = db.table("categoria").delete().eq("id_categoria", id_categoria).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error al eliminar la categoria")
    return None
