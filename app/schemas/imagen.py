from pydantic import BaseModel

class ImagenResponse(BaseModel):
    """Esquema de respuesta para la subida de imágenes"""
    url: str
    public_id: str
    mensaje: str = "Imagen subida exitosamente"
