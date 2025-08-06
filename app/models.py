from datetime import datetime, time
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, Boolean, Enum, TIMESTAMP, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, condecimal, EmailStr, validator
from typing import Optional, List
from .db import Base

# Modelos SQLAlchemy
class PlazaDB(Base):
    __tablename__ = 'plazas'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    estado = Column(String(20), default='activo')
    imagen_url = Column(String(500), nullable=True)
    imagen_public_id = Column(String(500), nullable=True)
    
    # Relación con locales
    locales = relationship("LocaleDB", back_populates="plaza", cascade="all, delete-orphan")

class LocaleDB(Base):
    __tablename__ = 'locales'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=True)
    direccion = Column(String(200), nullable=False)
    horario_apertura = Column(String(5), nullable=False)  # Formato: 'HH:MM'
    horario_cierre = Column(String(5), nullable=False)    # Formato: 'HH:MM'
    tipo_comercio = Column(String(50), nullable=False, default='otro')  # Ej: 'restaurante', 'cafeteria', 'tienda', 'servicio', 'otro'
    estado = Column(String(20), default='activo')
    imagen_url = Column(String(500), nullable=True)
    imagen_public_id = Column(String(500), nullable=True)
    plaza_id = Column(Integer, ForeignKey('plazas.id', ondelete='CASCADE'), nullable=False)
    id_gerente = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'), nullable=True)
    
    # Relaciones
    plaza = relationship("PlazaDB", back_populates="locales")
    gerente = relationship("UsuarioDB")
    pedidos = relationship("PedidoDB", back_populates="local", cascade="all, delete-orphan")

# Modelos Pydantic
class PlazaBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    direccion: str = Field(..., max_length=200)
    estado: str = Field('activo', max_length=20)
    imagen_url: Optional[str] = None
    imagen_public_id: Optional[str] = None

class PlazaCreate(PlazaBase):
    pass

class Plaza(PlazaBase):
    id: int
    
    class Config:
        from_attributes = True

class LocaleBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: str = Field(None, max_length=500)
    direccion: str = Field(..., max_length=200)
    horario_apertura: str = Field(..., pattern='^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')  # Formato HH:MM
    horario_cierre: str = Field(..., pattern='^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')    # Formato HH:MM
    tipo_comercio: str = Field('otro', max_length=50)  # Ej: 'restaurante', 'cafeteria', 'tienda', 'servicio', 'otro'
    estado: str = Field('activo', max_length=20)
    imagen_url: Optional[str] = None
    imagen_public_id: Optional[str] = None
    plaza_id: int
    id_gerente: Optional[int] = None
    
    @validator('tipo_comercio')
    def validate_tipo_comercio(cls, v):
        tipos_validos = ['restaurante', 'cafeteria', 'tienda', 'servicio', 'otro']
        if v.lower() not in tipos_validos:
            raise ValueError(f"Tipo de comercio no válido. Debe ser uno de: {', '.join(tipos_validos)}")
        return v.lower()
    
    @validator('id_gerente')
    def validate_gerente(cls, v, values, **kwargs):
        # Esta validación asume que hay acceso a la base de datos
        # La validación real se hará en los endpoints
        return v

class LocaleCreate(LocaleBase):
    pass

class Locale(LocaleBase):
    id: int
    
    class Config:
        from_attributes = True

# Modelos SQLAlchemy para Pedidos
# Modelo SQLAlchemy para Pedidos
class PedidoDB(Base):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    id_local = Column(Integer, ForeignKey('locales.id', ondelete='CASCADE'), nullable=False)
    fecha_pedido = Column(DateTime, server_default=func.now())
    estado_pedido = Column(Enum('pendiente', 'en_preparacion', 'listo_para_recoger', 'completado', 'cancelado', 
                              name='estados_pedido'), 
                          nullable=False, 
                          default='pendiente')
    total_pedido = Column(DECIMAL(10, 2), nullable=False)
    instrucciones_especiales = Column(Text, nullable=True)
    tiempo_preparacion_estimado = Column(Integer, nullable=False)  # en minutos
    
    # Relaciones
    usuario = relationship("UsuarioDB", back_populates="pedidos")
    local = relationship("LocaleDB", back_populates="pedidos")
    items = relationship("PedidoItemDB", back_populates="pedido", cascade="all, delete-orphan")

# Modelo SQLAlchemy para Ítems de Pedido
class PedidoItemDB(Base):
    __tablename__ = 'pedido_items'
    
    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id', ondelete='CASCADE'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id', ondelete='CASCADE'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    instrucciones_especiales = Column(Text, nullable=True)
    
    # Relaciones
    pedido = relationship("PedidoDB", back_populates="items")
    producto = relationship("ProductoDB")

# Modelos para Menús
class MenuDB(Base):
    __tablename__ = 'menus'
    
    id = Column(Integer, primary_key=True, index=True)
    id_local = Column(Integer, ForeignKey('locales.id', ondelete='CASCADE'), nullable=False)
    nombre_menu = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    
    # Relación con productos
    productos = relationship("ProductoDB", back_populates="menu", cascade="all, delete-orphan")

class ProductoDB(Base):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(DECIMAL(10, 2), nullable=False)
    id_menu = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), nullable=False)
    disponible = Column(Boolean, nullable=False, default=True)
    categoria = Column(String(50), nullable=True)
    imagen_url = Column(String(500), nullable=True)
    imagen_public_id = Column(String(500), nullable=True)
    
    # Relación con menú
    menu = relationship("MenuDB", back_populates="productos")

# Modelos Pydantic para Menús
class MenuBase(BaseModel):
    nombre_menu: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    id_local: int

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: int
    
    class Config:
        from_attributes = True

# Modelos Pydantic para Productos
class ProductoBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    precio: condecimal(gt=0, decimal_places=2)
    disponible: bool = Field(default=True, description="Si el producto está disponible para la venta")
    categoria: Optional[str] = Field(None, max_length=50)
    id_menu: int
    imagen_url: Optional[str] = None
    imagen_public_id: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    precio: Optional[condecimal(gt=0, decimal_places=2)] = None
    disponible: Optional[bool] = None
    categoria: Optional[str] = Field(None, max_length=50)
    id_menu: Optional[int] = None
    imagen_url: Optional[str] = None
    imagen_public_id: Optional[str] = None

class Producto(ProductoBase):
    id: int
    
    class Config:
        from_attributes = True

# Modelo para códigos de restablecimiento de contraseña
class ResetCodeDB(Base):
    __tablename__ = 'reset_codes'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, index=True)
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

# Modelo SQLAlchemy para Usuarios
class UsuarioDB(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)
    password = Column(String(255), nullable=False)
    rol = Column(String(20), default='usuario')
    estado = Column(String(20), default='activo')
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    imagen_url = Column(String(500), nullable=True)
    imagen_public_id = Column(String(500), nullable=True)
    
    # Relaciones
    pedidos = relationship("PedidoDB", back_populates="usuario", cascade="all, delete-orphan")

# Modelos Pydantic para Usuarios
class UsuarioBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    rol: str = "usuario"
    imagen_url: Optional[str] = None
    imagen_public_id: Optional[str] = None
    
    @validator('telefono')
    def validate_telefono(cls, v):
        if v is not None:
            # Remove any non-digit characters
            v = ''.join(filter(str.isdigit, v))
            # Add +52 prefix if not present and length is 10
            if len(v) == 10:
                v = f"+52{v}"
            elif not v.startswith('+') and len(v) > 10:
                v = f"+{v}"
        return v

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe contener al menos una mayúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    rol: Optional[str] = None
    estado: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

class Usuario(UsuarioBase):
    id: int
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True

# Modelos Pydantic para Pedidos
class PedidoItemBase(BaseModel):
    id_producto: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: condecimal(gt=0, decimal_places=2)
    instrucciones_especiales: Optional[str] = None

class PedidoItemCreate(PedidoItemBase):
    pass

class PedidoItemUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, gt=0)
    instrucciones_especiales: Optional[str] = None

class PedidoItem(PedidoItemBase):
    id: int
    id_pedido: int
    
    class Config:
        from_attributes = True

class PedidoBase(BaseModel):
    id_local: int
    instrucciones_especiales: Optional[str] = None
    items: List[PedidoItemCreate]

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(BaseModel):
    estado_pedido: Optional[str] = None
    instrucciones_especiales: Optional[str] = None
    tiempo_preparacion_estimado: Optional[int] = None

class Pedido(PedidoBase):
    id: int
    id_usuario: int
    fecha_pedido: datetime
    estado_pedido: str
    total_pedido: condecimal(gt=0, decimal_places=2)
    tiempo_preparacion_estimado: int
    items: List[PedidoItem] = []
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
