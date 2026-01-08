import os
import jwt
from fastapi import Depends, HTTPException,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from .database import get_supabase

security = HTTPBearer()

#validar el token JWT y obtener el usuario actual
async def get_current_user_id(credentials:HTTPAuthorizationCredentials=Depends(security))-> str:
   token = credentials.credentials
   try:
    payload=jwt.decode(
        token,
        os.getenv("JWT_SECRET_KEY"),
        algorithms=["HS256"],
        audience="authenticated"
    )
    user_id=payload.get("sub")
    if not user_id:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Usuario no autenticado")
    return user_id
   except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expirado")
   except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token inválido")
   

#obtener el id de la tienda actual del usuario
async def get_current_tienda_id(user_id:str= Depends(get_current_user_id),db:Client=Depends(get_supabase))-> int:
   response = db.table("tienda").select("id_tienda").eq("id_propietario",user_id).execute()
   if not response.data:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Tienda no encontrada para el usuario")
   return response.data[0]["id_tienda"]
