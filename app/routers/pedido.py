from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated, List, Optional
from ..database import get_supabase
from ..schemas.pedido import PedidoCreate, PedidoUpdateEstado, PedidoResponse
from supabase import Client
from ..dependencies import get_current_user_id, get_current_tienda_id

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

def get_db() -> Client:
    return get_supabase()

DbDependency = Annotated[Client, Depends(get_db)]

# Obtener todos los pedidos de las tiendas del usuario
@router.get("/", response_model=List[PedidoResponse])
def get_pedidos(db: DbDependency, user_id: str = Depends(get_current_user_id)):
    # Obtener todas las tiendas del propietario
    tiendas = db.table("tienda").select("id_tienda").eq("id_propietario", user_id).execute()
    
    if not tiendas.data:
        return []
    
    # Obtener los IDs de las tiendas
    ids_tiendas = [t["id_tienda"] for t in tiendas.data]
    
    # Filtrar pedidos por las tiendas del usuario
    pedidos = db.table("pedido").select("*").in_("id_tienda", ids_tiendas).execute()
    return pedidos.data



# Actualizar solo el estado del pedido
@router.patch("/{id_pedido}/estado", response_model=PedidoResponse)
def actualizar_estado_pedido(
    id_pedido: int, 
    estado_update: PedidoUpdateEstado, 
    db: DbDependency,
    user_id: str = Depends(get_current_user_id)
):
    # Primero verificar que el pedido exista
    pedido_existente = db.table("pedido").select("id_tienda").eq("id_pedido", id_pedido).execute()
    if not pedido_existente.data:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Obtener TODAS las tiendas del usuario
    tiendas_usuario = db.table("tienda").select("id_tienda").eq("id_propietario", user_id).execute()
    ids_tiendas = [t["id_tienda"] for t in tiendas_usuario.data]
    
    # Verificar que el pedido pertenezca a alguna tienda del usuario
    if pedido_existente.data[0]["id_tienda"] not in ids_tiendas:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este pedido")
    
    # Preparar los datos de actualización
    datos_update = {"estado": estado_update.estado}
    
    # Agregar fecha según el estado
    if estado_update.estado == "confirmado":
        datos_update["fecha_confirmacion"] = "now()"
    elif estado_update.estado == "entregado":
        datos_update["fecha_entrega"] = "now()"
    
    pedido_actualizado = db.table("pedido").update(datos_update).eq("id_pedido", id_pedido).execute()
    
    if not pedido_actualizado.data:
        raise HTTPException(status_code=500, detail="Error al actualizar el pedido")
    return pedido_actualizado.data[0]


#get pedido por estado
@router.get("/estado/{estado}", response_model=List[PedidoResponse])
def get_pedidos_por_estado(
    estado: str, 
    db: DbDependency,
    user_id: str = Depends(get_current_user_id)
):
    # Obtener todas las tiendas del propietario
    tiendas = db.table("tienda").select("id_tienda").eq("id_propietario", user_id).execute()
    
    if not tiendas.data:
        return []
    
    ids_tiendas = [t["id_tienda"] for t in tiendas.data]
    
    # Filtrar pedidos por estado y tiendas del usuario
    pedidos = db.table("pedido").select("*").eq("estado", estado).in_("id_tienda", ids_tiendas).execute()
    return pedidos.data