from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import cloudinary
import cloudinary.uploader

from ..db import get_db
from ..crud import get_plaza, update_plaza
from ..models import PlazaDB
from ..schemas import ImagenResponse
from ..services.cloudinary_service import upload_image, delete_image

router = APIRouter(prefix="/api/plazas", tags=["plazas"])

@router.post("/{plaza_id}/imagen", response_model=ImagenResponse)
async def subir_imagen_plaza(
    plaza_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Verificar que la plaza existe
    db_plaza = get_plaza(db, plaza_id=plaza_id)
    if not db_plaza:
        raise HTTPException(status_code=404, detail="Plaza no encontrada")
    
    # Verificar tipo de archivo
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos de imagen")
    
    try:
        # Subir imagen a Cloudinary
        upload_result = upload_image(
            await file.read(),
            folder="foodplaza/plazas",
            public_id=f"plaza_{plaza_id}"
        )
        
        # Si ya existe una imagen, eliminarla de Cloudinary
        if db_plaza.imagen_public_id:
            try:
                delete_image(db_plaza.imagen_public_id)
            except Exception as e:
                print(f"Error al eliminar imagen anterior: {str(e)}")
        
        # Actualizar la plaza con la nueva imagen
        update_data = {
            "imagen_url": upload_result["url"],
            "imagen_public_id": upload_result["public_id"]
        }
        update_plaza(db, plaza_id, update_data)
        
        return {
            "url": upload_result["url"],
            "public_id": upload_result["public_id"],
            "mensaje": "Imagen subida exitosamente"
        }
        
    except Exception as e:
        print(f"Error al subir imagen: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

@router.delete("/{plaza_id}/imagen")
async def eliminar_imagen_plaza(
    plaza_id: int,
    db: Session = Depends(get_db)
):
    # Verificar que la plaza existe
    db_plaza = get_plaza(db, plaza_id=plaza_id)
    if not db_plaza:
        raise HTTPException(status_code=404, detail="Plaza no encontrada")
    
    # Verificar si la plaza tiene una imagen
    if not db_plaza.imagen_public_id:
        raise HTTPException(status_code=404, detail="La plaza no tiene una imagen asociada")
    
    try:
        # Eliminar la imagen de Cloudinary
        delete_image(db_plaza.imagen_public_id)
        
        # Actualizar la plaza
        update_data = {
            "imagen_url": None,
            "imagen_public_id": None
        }
        update_plaza(db, plaza_id, update_data)
        
        return {"mensaje": "Imagen eliminada exitosamente"}
        
    except Exception as e:
        print(f"Error al eliminar imagen: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {str(e)}")
