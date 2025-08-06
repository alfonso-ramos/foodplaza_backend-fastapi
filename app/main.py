from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router
from app.routers.plazas_imagenes import router as plazas_imagenes_router
from app.routers.locales_imagenes import router as locales_imagenes_router
from app.routers.productos_imagenes import router as productos_imagenes_router
from app.routers.pedidos import router as pedidos_router
from app.routers.auth import router as auth_router
from app.db import create_tables

app = FastAPI()

# Configuración CORS básica
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(router, prefix="/api")
app.include_router(plazas_imagenes_router)
app.include_router(locales_imagenes_router)
app.include_router(productos_imagenes_router)
app.include_router(pedidos_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")

# Crear tablas al iniciar
@app.on_event("startup")
def startup():
    create_tables()
    print("Base de datos lista")

@app.get("/")
def read_root():
    return {"message": "API de plazas de comida"}