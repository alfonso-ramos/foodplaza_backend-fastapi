"""
Módulo para excepciones personalizadas de la aplicación.
"""
from fastapi import status
from fastapi.exceptions import HTTPException
from typing import Any, Dict, Optional

class BaseAPIException(HTTPException):
    """Excepción base para la API."""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Ha ocurrido un error inesperado"
    headers: Optional[Dict[str, str]] = None

    def __init__(
        self,
        detail: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> None:
        detail = detail or self.detail
        headers = headers or self.headers
        super().__init__(
            status_code=self.status_code,
            detail=detail,
            headers=headers,
            **kwargs
        )

# Errores de autenticación y autorización
class UnauthorizedError(BaseAPIException):
    """Error cuando las credenciales son inválidas o faltan."""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "No autorizado: credenciales inválidas o faltantes"

class ForbiddenError(BaseAPIException):
    """Error cuando el usuario no tiene permisos para acceder al recurso."""
    status_code = status.HTTP_403_FORBIDDEN
    detail = "No tiene permisos para acceder a este recurso"

# Errores de validación
class ValidationError(BaseAPIException):
    """Error cuando los datos de entrada no son válidos."""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Error de validación en los datos de entrada"

# Errores de recursos no encontrados
class NotFoundError(BaseAPIException):
    """Error cuando no se encuentra un recurso."""
    status_code = status.HTTP_404_NOT_FOUND
    detail = "El recurso solicitado no fue encontrado"

# Errores de conflicto
class ConflictError(BaseAPIException):
    """Error cuando hay un conflicto con el estado actual del recurso."""
    status_code = status.HTTP_409_CONFLICT
    detail = "Conflicto con el estado actual del recurso"

# Errores de negocio
class BusinessRuleError(BaseAPIException):
    """Error cuando se viola una regla de negocio."""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Error en la regla de negocio"

# Manejador global de excepciones
async def global_exception_handler(request, exc):
    """
    Manejador global de excepciones para la API.
    
    Args:
        request: La solicitud que generó la excepción
        exc: La excepción que se generó
        
    Returns:
        Respuesta HTTP con el error correspondiente
    """
    if isinstance(exc, BaseAPIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers
        )
    
    # Manejar excepciones de FastAPI
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers
        )
    
    # Manejar excepciones de validación de Pydantic
    if hasattr(exc, "errors"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Error de validación", "errors": exc.errors()}
        )
    
    # Manejar cualquier otra excepción no controlada
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Error interno del servidor"}
    )
