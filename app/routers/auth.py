from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..db import get_db
from ..services.password_reset_service import PasswordResetService
from ..services.email.email_service import email_service
from ..crud import usuarios as crud_usuarios

router = APIRouter(tags=["auth"])

@router.post(
    "/password-reset/request",
    summary="Solicitar restablecimiento de contraseña",
    response_model=schemas.PasswordResetResponse,
    responses={
        200: {
            "description": "Código de verificación enviado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Se ha enviado un código de verificación a tu correo electrónico",
                        "email": "usuario@ejemplo.com"
                    }
                }
            }
        },
        404: {
            "description": "No existe una cuenta con este correo electrónico",
            "content": {
                "application/json": {
                    "example": {"detail": "No existe una cuenta con este correo electrónico"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Ocurrió un error al procesar tu solicitud"}
                }
            }
        }
    }
)
async def request_password_reset(
    request: schemas.PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Inicia el proceso de restablecimiento de contraseña enviando un código de verificación al correo electrónico del usuario.
    
    ### Cuerpo de la solicitud (application/json):
    ```json
    {
        "email": "usuario@ejemplo.com"
    }
    ```
    
    ### Respuestas:
    - **200 OK**: El código de verificación ha sido enviado al correo electrónico si existe una cuenta asociada.
    - **404 Not Found**: No existe una cuenta con el correo electrónico proporcionado.
    - **500 Internal Server Error**: Error inesperado al procesar la solicitud.
    
    ### Detalles adicionales:
    - El código de verificación es numérico de 6 dígitos.
    - El código expira después de 15 minutos (configurable).
    - Cada código solo puede ser utilizado una vez.
    - Por razones de seguridad, el mensaje de éxito es genérico.
    """
    # Verificar si el correo existe
    user = crud_usuarios.get_usuario_by_email(db, email=request.email)
    if not user:
        # Opción 1: No revelar si el correo existe (más seguro)
        # return {"message": "Si el correo existe, se ha enviado un código de verificación"}
        
        # Opción 2: Mostrar que el correo no existe (menos seguro pero más claro para el usuario)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe una cuenta con este correo electrónico"
        )
    
    try:
        # Generar y guardar el código de restablecimiento
        reset_service = PasswordResetService(db)
        reset_code = reset_service.create_reset_code(email=request.email)
        
        # Enviar el código por correo electrónico
        await email_service.send_verification_code(
            to_email=request.email,
            verification_code=reset_code.code
        )
        
        return {
            "message": "Se ha enviado un código de verificación a tu correo electrónico",
            "email": request.email
        }
    except Exception as e:
        # Registrar el error para depuración
        print(f"Error al enviar el correo de restablecimiento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al procesar tu solicitud"
        )

@router.post(
    "/password-reset/verify",
    summary="Verificar código y actualizar contraseña",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Contraseña actualizada exitosamente",
            "content": {
                "application/json": {
                    "example": {"message": "Contraseña actualizada exitosamente"}
                }
            }
        },
        400: {
            "description": "Solicitud inválida",
            "content": {
                "application/json": {
                    "examples": {
                        "Código inválido": {"detail": "Código de verificación inválido"},
                        "Código expirado": {"detail": "El código de verificación ha expirado"},
                        "Código ya utilizado": {"detail": "Este código ya ha sido utilizado"},
                        "Contraseña inválida": {"detail": "La contraseña no cumple con los requisitos mínimos"}
                    }
                }
            }
        },
        404: {
            "description": "No existe una cuenta con este correo electrónico",
            "content": {
                "application/json": {
                    "example": {"detail": "No existe una cuenta con este correo electrónico"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Ocurrió un error al actualizar la contraseña"}
                }
            }
        }
    }
)
async def verify_reset_code(
    request: schemas.PasswordResetVerify,
    db: Session = Depends(get_db)
):
    """
    Verifica el código de restablecimiento y actualiza la contraseña del usuario.
    
    ### Cuerpo de la solicitud (application/json):
    ```json
    {
        "email": "usuario@ejemplo.com",
        "code": "123456",
        "new_password": "NuevaContraseña123"
    }
    ```
    
    ### Respuestas:
    - **200 OK**: Contraseña actualizada exitosamente.
    - **400 Bad Request**:
      - Código de verificación inválido
      - Código expirado
      - Código ya utilizado
      - La nueva contraseña no cumple con los requisitos
    - **404 Not Found**: No existe una cuenta con el correo electrónico proporcionado.
    - **500 Internal Server Error**: Error inesperado al procesar la solicitud.
    
    ### Requisitos de la contraseña:
    - Mínimo 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número
    """
    reset_service = PasswordResetService(db)
    
    # Verificar si el código es válido
    if not reset_service.verify_reset_code(email=request.email, code=request.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código de verificación inválido o expirado"
        )
    
    # Obtener el usuario
    user = crud_usuarios.get_usuario_by_email(db, email=request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Actualizar la contraseña
    update_data = {"password": request.new_password}
    crud_usuarios.update_usuario(db, user.id, update_data)
    
    return {"message": "Contraseña actualizada exitosamente"}
