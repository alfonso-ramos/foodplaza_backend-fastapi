
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from typing import List
from sqlalchemy.orm import Session

from app import schemas
from app.crud import imagenes as crud_imagenes
from app.services.storage import storage_service
from app.db import get_db

router = APIRouter(tags=["imagenes"], responses={404: {"description": "Not found"}},)

ALLOWED_ENTITY_TYPES = ["plaza", "local", "producto", "usuario"]

@router.post("/upload/{tipo_entidad}/{entidad_id}", response_model=schemas.imagenes.Imagen, status_code=status.HTTP_201_CREATED, summary="Upload a new image for an entity")
async def upload_imagen(
    tipo_entidad: str,
    entidad_id: int,
    file: UploadFile = File(...),
    es_principal: bool = False,
    orden: int = 0,
    db: Session = Depends(get_db),
):
    """
    Upload a new image for a specific entity (plaza, local, product, or user).

    - **tipo_entidad**: Type of entity (plaza, local, product, user)
    - **entidad_id**: ID of the entity
    - **file**: Image file to upload
    - **es_principal**: If True, this image will be marked as the main one for the entity
    - **orden**: Display order of the image (lower = first)
    """
    if tipo_entidad.lower() not in ALLOWED_ENTITY_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid entity type. Must be one of: {', '.join(ALLOWED_ENTITY_TYPES)}"
        )

    try:
        subfolder = f"{tipo_entidad}s/{entidad_id}"
        file_path, filename = await storage_service.save_upload_file(file, subfolder)

        imagen_data = schemas.imagenes.ImagenCreate(
            tipo_entidad=tipo_entidad.lower(),
            entidad_id=entidad_id,
            es_principal=es_principal,
            orden=orden,
            metadata={
                "original_filename": file.filename,
                "content_type": file.content_type,
                "size": file.size,
            }
        )

        db_imagen = crud_imagenes.create_imagen(db, imagen_data, file_path)
        return db_imagen

    except HTTPException as he:
        raise he
    except Exception as e:
        if 'file_path' in locals():
            storage_service.delete_file(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing the image: {str(e)}"
        )

@router.get("/{tipo_entidad}/{entidad_id}", response_model=List[schemas.imagenes.Imagen], summary="Get all images for an entity")
def get_imagenes_entidad(
    tipo_entidad: str,
    entidad_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all images associated with a specific entity.
    """
    if tipo_entidad.lower() not in ALLOWED_ENTITY_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid entity type. Must be one of: {', '.join(ALLOWED_ENTITY_TYPES)}"
        )

    return crud_imagenes.get_imagenes_entidad(
        db, 
        tipo_entidad=tipo_entidad.lower(),
        entidad_id=entidad_id,
        skip=skip,
        limit=limit
    )

@router.get("/{tipo_entidad}/{entidad_id}/principal", response_model=schemas.imagenes.Imagen, summary="Get the main image for an entity")
def get_imagen_principal(
    tipo_entidad: str,
    entidad_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the main image for a specific entity.
    """
    if tipo_entidad.lower() not in ALLOWED_ENTITY_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid entity type. Must be one of: {', '.join(ALLOWED_ENTITY_TYPES)}"
        )

    db_imagen = crud_imagenes.get_imagen_principal(
        db, 
        tipo_entidad=tipo_entidad.lower(),
        entidad_id=entidad_id
    )

    if not db_imagen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No main image found for this entity"
        )

    return db_imagen

@router.put("/{imagen_id}", response_model=schemas.imagenes.Imagen, summary="Update image metadata")
def update_imagen(
    imagen_id: int,
    imagen: schemas.imagenes.ImagenUpdate,
    db: Session = Depends(get_db),
):
    """
    Update the metadata of an existing image.
    """
    db_imagen = crud_imagenes.get_imagen(db, imagen_id=imagen_id)
    if not db_imagen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    return crud_imagenes.update_imagen(db, db_imagen=db_imagen, imagen=imagen)

@router.delete("/{imagen_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an image")
def delete_imagen(
    imagen_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an image from the system.
    """
    db_imagen = crud_imagenes.get_imagen(db, imagen_id=imagen_id)
    if not db_imagen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    if db_imagen.url and storage_service.get_file_path(db_imagen.url):
        storage_service.delete_file(db_imagen.url)

    crud_imagenes.delete_imagen(db, db_imagen=db_imagen)

    return {"ok": True}

