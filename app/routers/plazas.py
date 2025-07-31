from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.plazas import Plaza, PlazaCreate, PlazaUpdate
from app.crud.plazas import (
    get_plaza,
    get_plazas,
    create_plaza,
    update_plaza,
    delete_plaza
)

router = APIRouter(tags=["plazas"])

@router.get(
    "/{plaza_id}",
    response_model=Plaza,
    summary="Obtener una plaza por ID",
    description="Obtiene los detalles de una plaza específica por su ID.",
    responses={
        200: {"description": "Plaza encontrada exitosamente"},
        404: {"description": "Plaza no encontrada"}
    }
)
async def read_plaza(plaza_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una plaza específica por su ID.
    """
    db_plaza = get_plaza(db, plaza_id=plaza_id)
    if db_plaza is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plaza no encontrada"
        )
    return db_plaza

@router.get(
    "/",
    response_model=List[Plaza],
    summary="Listar todas las plazas",
    description="Obtiene una lista de todas las plazas con paginación.",
    responses={
        200: {"description": "Lista de plazas obtenida exitosamente"}
    }
)
async def read_plazas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista paginada de todas las plazas.
    """
    return get_plazas(db, skip=skip, limit=limit)

@router.post(
    "/",
    response_model=Plaza,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva plaza",
    description="Crea una nueva plaza con los datos proporcionados.",
    responses={
        201: {"description": "Plaza creada exitosamente"},
        400: {"description": "Datos de entrada inválidos"}
    }
)
def create_new_plaza(
    plaza: PlazaCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva plaza con los datos proporcionados.
    """
    try:
        return create_plaza(db=db, plaza=plaza)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al crear la plaza: {str(e)}"
        )

@router.put(
    "/{plaza_id}",
    response_model=Plaza,
    summary="Actualizar una plaza existente",
    description="Actualiza los datos de una plaza existente.",
    responses={
        200: {"description": "Plaza actualizada exitosamente"},
        404: {"description": "Plaza no encontrada"},
        400: {"description": "Datos de entrada inválidos"}
    }
)
async def update_existing_plaza(
    plaza_id: int,
    plaza: PlazaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos de una plaza existente.
    """
    try:
        db_plaza = update_plaza(
            db=db,
            plaza_id=plaza_id,
            plaza_data=plaza.dict(exclude_unset=True)
        )
        if db_plaza is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plaza no encontrada"
            )
        return db_plaza
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar la plaza: {str(e)}"
        )

@router.delete(
    "/{plaza_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una plaza",
    description="Elimina una plaza por su ID.",
    responses={
        204: {"description": "Plaza eliminada exitosamente"},
        404: {"description": "Plaza no encontrada"}
    }
)
async def delete_existing_plaza(
    plaza_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una plaza por su ID.
    """
    success = delete_plaza(db=db, plaza_id=plaza_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plaza no encontrada"
        )
    return None
