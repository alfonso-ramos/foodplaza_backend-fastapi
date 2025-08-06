from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime, timedelta

class PasswordResetRequest(BaseModel):
    """Esquema para solicitar un restablecimiento de contraseña"""
    email: EmailStr = Field(..., description="Correo electrónico del usuario")

class PasswordResetVerify(BaseModel):
    """Esquema para verificar el código de restablecimiento"""
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    code: str = Field(..., min_length=6, max_length=6, pattern=r'^\d{6}$', description="Código de verificación de 6 dígitos")
    new_password: str = Field(..., min_length=8, description="Nueva contraseña (mínimo 8 caracteres)")

    @validator('new_password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not any(char.isdigit() for char in v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not any(char.isupper() for char in v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not any(char.islower() for char in v):
            raise ValueError('La contraseña debe contener al menos una letra minúscula')
        return v

class ResetCodeInDB(PasswordResetRequest):
    """Esquema para el código de restablecimiento en la base de datos"""
    code: str = Field(..., description="Código de verificación")
    expires_at: datetime = Field(..., description="Fecha y hora de expiración del código")
    used: bool = Field(default=False, description="Indica si el código ya fue utilizado")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha y hora de creación del código")

class PasswordResetResponse(BaseModel):
    """Esquema para la respuesta de la solicitud de restablecimiento de contraseña"""
    message: str = Field(..., description="Mensaje descriptivo del resultado de la operación")
    email: EmailStr = Field(..., description="Correo electrónico al que se envió el código de verificación")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Se ha enviado un código de verificación a tu correo electrónico",
                "email": "usuario@ejemplo.com"
            }
        }
