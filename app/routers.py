from fastapi import APIRouter
from app.schemas.plazas import router as plazas_router
from app.schemas.locales import router as locales_router
from app.routers.menus import router as menus_router
from app.routers.productos import router as productos_router

# Create the main router
router = APIRouter()

# Include the routers from different modules
router.include_router(plazas_router, prefix="/plazas", tags=["plazas"])
router.include_router(locales_router, prefix="/locales", tags=["locales"])
router.include_router(menus_router, tags=["menus"])
router.include_router(productos_router, tags=["productos"])