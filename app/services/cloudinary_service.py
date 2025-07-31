import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image(file, folder: str, public_id: str = None):
    """
    Sube una imagen a Cloudinary
    
    Args:
        file: Archivo a subir (BytesIO o ruta)
        folder: Carpeta en Cloudinary (ej: 'usuarios', 'productos')
        public_id: ID público opcional para la imagen
        
    Returns:
        dict: Diccionario con 'url' y 'public_id' de la imagen
    """
    try:
        upload_result = cloudinary.uploader.upload(
            file,
            folder=f"foodplaza/{folder}",
            public_id=public_id,
            resource_type="auto"
        )
        
        return {
            "url": upload_result.get('secure_url'),
            "public_id": upload_result.get('public_id')
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir la imagen: {str(e)}"
        )

def delete_image(public_id: str):
    """
    Elimina una imagen de Cloudinary
    
    Args:
        public_id: ID público de la imagen a eliminar
    """
    try:
        if public_id:
            cloudinary.uploader.destroy(public_id)
    except Exception as e:
        # No lanzamos excepción para no afectar el flujo principal
        print(f"Error al eliminar imagen de Cloudinary: {str(e)}")

def get_image_url(public_id: str, width: int = None, height: int = None):
    """
    Genera la URL de una imagen con transformaciones opcionales
    
    Args:
        public_id: ID público de la imagen
        width: Ancho deseado (opcional)
        height: Alto deseado (opcional)
        
    Returns:
        str: URL de la imagen
    """
    if not public_id:
        return None
        
    transformations = {
        'quality': 'auto',
        'fetch_format': 'auto'
    }
    
    if width and height:
        transformations.update({
            'width': width,
            'height': height,
            'crop': 'fill'
        })
    
    url, _ = cloudinary.utils.cloudinary_url(
        public_id,
        **transformations
    )
    
    return url
