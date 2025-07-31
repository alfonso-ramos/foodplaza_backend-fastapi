from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import cloudinary
import cloudinary.uploader

from ..db import get_db
from ..crud import get_producto, update_producto
from ..models import ProductoDB
from ..schemas import ImagenResponse
from ..services.cloudinary_service import upload_image, delete_image

router = APIRouter(prefix="/api/productos", tags=["productos"])

@router.post("/{producto_id}/imagen", response_model=ImagenResponse)
async def subir_imagen_producto(
    producto_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Verificar que el producto existe
    db_producto = get_producto(db, producto_id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar tipo de archivo
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos de imagen")
    
    try:
        # Subir imagen a Cloudinary
        upload_result = upload_image(
            await file.read(),
            folder="foodplaza/productos",
            public_id=f"producto_{producto_id}"
        )
        
        # Si ya existe una imagen, eliminarla de Cloudinary
        if db_producto.imagen_public_id:
            try:
                delete_image(db_producto.imagen_public_id)
            except Exception as e:
                print(f"Error al eliminar imagen anterior: {str(e)}")
        
        # Actualizar el producto con la nueva imagen
        update_data = {
            "imagen_url": upload_result["url"],
            "imagen_public_id": upload_result["public_id"]
        }
        update_producto(db, producto_id, update_data)
        
        return {
            "url": upload_result["url"],
            "public_id": upload_result["public_id"],
            "mensaje": "Imagen subida exitosamente"
        }
        
    except Exception as e:
        print(f"Error al subir imagen: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

@router.delete("/{producto_id}/imagen")
async def eliminar_imagen_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    # Verificar que el producto existe
    db_producto = get_producto(db, producto_id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar si el producto tiene una imagen
    if not db_producto.imagen_public_id:
        raise HTTPException(status_code=404, detail="El producto no tiene una imagen asociada")
    
    try:
        # Eliminar la imagen de Cloudinary
        delete_image(db_producto.imagen_public_id)
        
        # Actualizar el producto
        update_data = {
            "imagen_url": None,
            "imagen_public_id": None
        }
        update_producto(db, producto_id, update_data)
        
        return {"mensaje": "Imagen eliminada exitosamente"}
        
    except Exception as e:
        print(f"Error al eliminar imagen: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {str(e)}")
