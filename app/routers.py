from fastapi import APIRouter
from .schemas.plazas import router as plazas_router
from .schemas.locales import router as locales_router

# Create the main router
router = APIRouter()

# Include the routers from different modules
router.include_router(plazas_router, prefix="/plazas", tags=["plazas"])
router.include_router(locales_router, prefix="/locales", tags=["locales"])