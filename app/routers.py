
from fastapi import APIRouter
from .schemas.plazas import router as plazas_router

# Create the main router
router = APIRouter()

# Include the routers from different modules
router.include_router(plazas_router, prefix="/plazas", tags=["plazas"])