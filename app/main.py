from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, usuarios, plazas, locales, menus, productos, imagenes
from app.db import create_tables
from app.core.config import settings

# Create database tables on startup
create_tables()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

api_router = APIRouter(prefix=settings.API_V1_STR)

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(plazas.router, prefix="/plazas", tags=["plazas"])
api_router.include_router(locales.router, prefix="/locales", tags=["locales"])
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(productos.router, prefix="/productos", tags=["productos"])
api_router.include_router(imagenes.router, prefix="/imagenes", tags=["imagenes"])

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}