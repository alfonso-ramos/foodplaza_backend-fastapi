from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, model_validator
from typing import Optional, List
from datetime import datetime

from .enums import TipoUsuario, EstadoUsuario

class UsuarioBase(BaseModel):
    """
    Esquema base para los usuarios. Contiene los campos comunes para todas las operaciones.
    """
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    nombre: str = Field(..., max_length=100, description="Nombre del usuario")
    apellido: str = Field(..., max_length=100, description="Apellido del usuario")
    telefono: Optional[str] = Field(
        None, 
        min_length=8, 
        max_length=20, 
        pattern=r"^\+?[0-9\s-]+$",
        description="Número de teléfono del usuario (formato internacional)"
    )
    direccion: Optional[str] = Field(
        None, 
        max_length=200, 
        description="Dirección física del usuario"
    )
    tipo: TipoUsuario = Field(
        default=TipoUsuario.CLIENTE, 
        description="Rol o tipo de usuario en el sistema"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "usuario@ejemplo.com",
                "nombre": "Juan",
                "apellido": "Pérez",
                "telefono": "+56912345678",
                "direccion": "Calle Falsa 123",
                "tipo": "cliente"
            }
        }
    )

class UsuarioCreate(UsuarioBase):
    """
    Esquema para la creación de un nuevo usuario.
    Incluye validación de contraseña.
    """
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=100,
        description="Contraseña del usuario (mínimo 8 caracteres, debe incluir mayúsculas, minúsculas y números)"
    )

    @field_validator('password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        if not any(c.islower() for c in v):
            raise ValueError("La contraseña debe contener al menos una letra minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe contener al menos un número")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "usuario@ejemplo.com",
                "nombre": "Juan",
                "apellido": "Pérez",
                "telefono": "+56912345678",
                "direccion": "Calle Falsa 123",
                "tipo": "cliente",
                "password": "ContraseñaSegura123"
            }
        }
    )

class UsuarioUpdate(BaseModel):
    """
    Esquema para actualizar un usuario existente.
    Todos los campos son opcionales.
    """
    email: Optional[EmailStr] = Field(None, description="Nuevo correo electrónico")
    nombre: Optional[str] = Field(None, max_length=100, description="Nuevo nombre")
    apellido: Optional[str] = Field(None, max_length=100, description="Nuevo apellido")
    telefono: Optional[str] = Field(
        None, 
        min_length=8, 
        max_length=20, 
        pattern=r"^\+?[0-9\s-]+$",
        description="Nuevo número de teléfono"
    )
    direccion: Optional[str] = Field(None, max_length=200, description="Nueva dirección")
    tipo: Optional[TipoUsuario] = Field(None, description="Nuevo tipo de usuario")
    estado: Optional[EstadoUsuario] = Field(None, description="Nuevo estado del usuario")

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        if not any([
            self.email is not None,
            self.nombre is not None,
            self.apellido is not None,
            self.telefono is not None,
            self.direccion is not None,
            self.tipo is not None,
            self.estado is not None
        ]):
            raise ValueError("Al menos un campo debe ser proporcionado para la actualización")
        return self

class UsuarioLogin(BaseModel):
    """
    Esquema para el inicio de sesión de un usuario.
    """
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "usuario@ejemplo.com",
                "password": "ContraseñaSegura123"
            }
        }
    )

class UsuarioInDBBase(UsuarioBase):
    """
    Esquema base para usuarios en la base de datos.
    Incluye campos adicionales generados por el sistema.
    """
    id: int = Field(..., description="Identificador único del usuario")
    estado: EstadoUsuario = Field(..., description="Estado actual del usuario")
    fecha_creacion: datetime = Field(..., description="Fecha de creación del usuario")
    ultimo_acceso: Optional[datetime] = Field(None, description="Fecha del último acceso")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "usuario@ejemplo.com",
                "nombre": "Juan",
                "apellido": "Pérez",
                "telefono": "+56912345678",
                "direccion": "Calle Falsa 123",
                "tipo": "cliente",
                "estado": "activo",
                "fecha_creacion": "2023-01-01T12:00:00Z",
                "ultimo_acceso": "2023-01-01T12:00:00Z"
            }
        }
    )

class Usuario(UsuarioInDBBase):
    """
    Esquema para devolver información de usuario.
    No incluye información sensible como contraseñas.
    """
    pass

class UsuarioWithToken(BaseModel):
    """
    Esquema para la respuesta de inicio de sesión exitoso.
    Incluye el token de acceso y la información del usuario.
    """
    access_token: str = Field(..., description="Token de acceso JWT")
    token_type: str = Field("bearer", description="Tipo de token")
    user: Usuario = Field(..., description="Información del usuario autenticado")

class UsuarioChangePassword(BaseModel):
    """
    Esquema para el cambio de contraseña de un usuario.
    """
    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(..., min_length=8, max_length=100, description="Nueva contraseña")

    @field_validator('new_password')
    def validate_new_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("La nueva contraseña debe tener al menos 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("La nueva contraseña debe contener al menos una letra mayúscula")
        if not any(c.islower() for c in v):
            raise ValueError("La nueva contraseña debe contener al menos una letra minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La nueva contraseña debe contener al menos un número")
        return v

class UserInfo(BaseModel):
    """
    Información básica del usuario para incluir en el token JWT.
    """
    id: int = Field(..., description="ID del usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    nombre: str = Field(..., description="Nombre del usuario")
    apellido: str = Field(..., description="Apellido del usuario")
    tipo: TipoUsuario = Field(..., description="Tipo de usuario")
    scopes: List[str] = Field(default_factory=list, description="Permisos del usuario")

class Token(BaseModel):
    """
    Esquema para la respuesta de autenticación exitosa.
    Incluye el token de acceso, token de actualización e información del usuario.
    """
    access_token: str = Field(..., description="Token de acceso JWT")
    token_type: str = Field("bearer", description="Tipo de token")
    refresh_token: str = Field(..., description="Token para renovar el acceso")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")
    user: UserInfo = Field(..., description="Información del usuario autenticado")
