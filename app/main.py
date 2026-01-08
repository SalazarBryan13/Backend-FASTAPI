from multiprocessing.dummy.connection import Client
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware

from .database import get_supabase
from .routers.tienda import router as tienda_router
from .routers.inventario import router as inventario_router
from .routers.categoria import router as categoria_router
from .routers.producto import router as producto_router
from .routers.pedido import router as pedido_router

app = FastAPI(title="API Móviles - Tiendas")

# Configuración de CORS para permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier URL
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tienda_router)
app.include_router(inventario_router)
app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(pedido_router)
