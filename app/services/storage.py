import os
import uuid
import shutil
from pathlib import Path
from typing import Optional, Tuple, BinaryIO
from fastapi import UploadFile, HTTPException, status


class StorageService:
    """Servicio para manejar el almacenamiento de archivos."""
    
    def __init__(self, upload_dir: str = None):
        """Inicializa el servicio de almacenamiento.
        
        Args:
            upload_dir: Directorio base para las cargas. Si no se especifica, se usa el de configuración.
        """
        self.upload_dir = Path(upload_dir) if upload_dir else Path("uploads")
        self.allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        self.max_file_size = 5 * 1024 * 1024  # 5MB
    
    async def save_upload_file(
        self, 
        file: UploadFile, 
        subfolder: str = ""
    ) -> Tuple[str, str]:
        """Guarda un archivo subido en el sistema de archivos.
        
        Args:
            file: Archivo subido a través de FastAPI
            subfolder: Subcarpeta donde guardar el archivo (ej: 'productos', 'usuarios')
            
        Returns:
            Tuple con (ruta_relativa, nombre_archivo)
            
        Raises:
            HTTPException: Si el archivo no es válido o hay un error al guardarlo
        """
        # Validar extensión del archivo
        file_extension = Path(file.filename).suffix.lower()[1:]  # Sin el punto
        if file_extension not in self.allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de archivo no permitido. Extensiones permitidas: {', '.join(self.allowed_extensions)}"
            )
        
        # Validar tamaño del archivo
        file.file.seek(0, 2)  # Ir al final del archivo
        file_size = file.file.tell()
        file.file.seek(0)  # Volver al inicio
        
        if file_size > self.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Archivo demasiado grande. Tamaño máximo permitido: {self.max_file_size / (1024 * 1024)}MB"
            )
        
        # Crear directorio de destino si no existe
        save_dir = self.upload_dir / subfolder
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar nombre único para el archivo
        file_uuid = str(uuid.uuid4())
        filename = f"{file_uuid}.{file_extension}"
        file_path = save_dir / filename
        
        try:
            # Guardar el archivo
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Devolver la ruta relativa al directorio de subidas
            relative_path = str(Path(subfolder) / filename) if subfolder else filename
            return str(relative_path), filename
            
        except Exception as e:
            # En caso de error, intentar eliminar el archivo si se creó parcialmente
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al guardar el archivo: {str(e)}"
            )
    
    def delete_file(self, filepath: str) -> bool:
        """Elimina un archivo del sistema de archivos.
        
        Args:
            filepath: Ruta relativa al directorio de subidas
            
        Returns:
            bool: True si se eliminó correctamente, False si el archivo no existía
        """
        full_path = self.upload_dir / filepath
        
        try:
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def get_file_path(self, filepath: str) -> Optional[Path]:
        """Obtiene la ruta completa de un archivo.
        
        Args:
            filepath: Ruta relativa al directorio de subidas
            
        Returns:
            Path: Ruta completa al archivo o None si no existe
        """
        full_path = self.upload_dir / filepath
        return full_path if full_path.exists() else None

# Instancia global del servicio de almacenamiento
storage_service = StorageService()
