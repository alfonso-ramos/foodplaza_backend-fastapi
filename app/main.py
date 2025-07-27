from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router
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

# Crear tablas al iniciar
@app.on_event("startup")
def startup():
    create_tables()
    print("Base de datos lista")

@app.get("/")
def read_root():
    return {"message": "API de plazas de comida"}