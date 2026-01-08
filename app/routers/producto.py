from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated, List
from ..database import get_supabase
from ..schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from supabase import Client
from ..dependencies import get_current_tienda_id, get_current_user_id

router = APIRouter(prefix="/productos", tags=["productos"])


def get_db() -> Client:
    return get_supabase()


DbDependency = Annotated[Client, Depends(get_db)]


#obtener productos de las tiendas del usuario
@router.get("/{id_tienda}", response_model=List[ProductoResponse])
def get_productos(db: DbDependency, id_tienda: int):
    # Obtener todas las tiendas del propietario
    Productos= db.table("producto").select("*").eq("id_tienda", id_tienda).execute()
    return Productos.data
   






#crear producto
@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(db: DbDependency, producto: ProductoCreate):
    datos = producto.model_dump()
    datos["precio"] = float(datos["precio"])  # Convertir Decimal a float para JSON
    nuevo_producto = db.table("producto").insert(datos).execute()
    if not nuevo_producto.data:
        raise HTTPException(status_code=400, detail="Error al crear el producto")
    return nuevo_producto.data[0]


#actualizar producto
@router.put("/{id_producto}", response_model=ProductoResponse, status_code=200)
def actualizar_producto(db: DbDependency, id_producto: int, producto_update: ProductoUpdate):
    datos = producto_update.model_dump(exclude_unset=True)
    if "precio" in datos and datos["precio"] is not None:
        datos["precio"] = float(datos["precio"])  # Convertir Decimal a float para JSON
    producto_actualizado = db.table("producto").update(datos).eq("id_producto", id_producto).execute()
    if not producto_actualizado.data:
        raise HTTPException(status_code=400, detail="Error al actualizar el producto")
    return producto_actualizado.data[0]


#eliminar producto
@router.delete("/{id_producto}", status_code=204)
def eliminar_producto(db: DbDependency, id_producto: int):
    response = db.table("producto").delete().eq("id_producto", id_producto).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error al eliminar el producto")
    return None
