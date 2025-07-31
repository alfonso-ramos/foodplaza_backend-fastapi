from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import cloudinary
import cloudinary.uploader

from ..db import get_db
from ..crud import get_locale, update_locale
from ..models import LocaleDB
from ..schemas import ImagenResponse
from ..services.cloudinary_service import upload_image, delete_image

router = APIRouter(prefix="/api/locales", tags=["locales"])

@router.post("/{local_id}/imagen", response_model=ImagenResponse)
async def subir_imagen_local(
    local_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Verificar que el local existe
    db_local = get_locale(db, local_id=local_id)
    if not db_local:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    
    # Verificar tipo de archivo
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos de imagen")
    
    try:
        # Subir imagen a Cloudinary
        upload_result = upload_image(
            await file.read(),
            folder="foodplaza/locales",
            public_id=f"local_{local_id}"
        )
        
        # Si ya existe una imagen, eliminarla de Cloudinary
        if db_local.imagen_public_id:
            try:
                delete_image(db_local.imagen_public_id)
            except Exception as e:
                print(f"Error al eliminar imagen anterior: {str(e)}")
        
        # Actualizar el local con la nueva imagen
        update_data = {
            "imagen_url": upload_result["url"],
            "imagen_public_id": upload_result["public_id"]
        }
        update_locale(db, local_id, update_data)
        
        return {
            "url": upload_result["url"],
            "public_id": upload_result["public_id"],
            "mensaje": "Imagen subida exitosamente"
        }
        
    except Exception as e:
        print(f"Error al subir imagen: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

@router.delete("/{local_id}/imagen")
async def eliminar_imagen_local(
    local_id: int,
    db: Session = Depends(get_db)
):
    # Verificar que el local existe
    db_local = get_locale(db, local_id=local_id)
    if not db_local:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    
    # Verificar si el local tiene una imagen
    if not db_local.imagen_public_id:
        raise HTTPException(status_code=404, detail="El local no tiene una imagen asociada")
    
    try:
        # Eliminar la imagen de Cloudinary
        delete_image(db_local.imagen_public_id)
        
        # Actualizar el local
        update_data = {
            "imagen_url": None,
            "imagen_public_id": None
        }
        update_locale(db, local_id, update_data)
        
        return {"mensaje": "Imagen eliminada exitosamente"}
        
    except Exception as e:
        print(f"Error al eliminar imagen: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {str(e)}")
