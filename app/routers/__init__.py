from fastapi import APIRouter
from . import plazas, locales, menus, productos, usuarios

# Crear el router principal
router = APIRouter()

# Incluir los routers de los diferentes módulos
router.include_router(plazas.router, prefix="/plazas", tags=["plazas"])
router.include_router(locales.router, prefix="/locales", tags=["locales"])
router.include_router(menus.router, prefix="/menus", tags=["menus"])
router.include_router(productos.router, prefix="/productos", tags=["productos"])
router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])

# Exportar el router para que pueda ser importado desde otros módulos
__all__ = ["router"]
