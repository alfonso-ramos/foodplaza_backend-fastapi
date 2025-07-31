from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
from ..schemas.enums import TipoUsuario, EstadoUsuario

class UsuarioDB(Base):
    """
    Modelo de base de datos para la tabla de usuarios.
    
    Atributos:
        id: Identificador único del usuario
        email: Correo electrónico del usuario (único)
        nombre: Nombre del usuario
        apellido: Apellido del usuario
        hashed_password: Contraseña hasheada
        telefono: Número de teléfono (opcional)
        direccion: Dirección del usuario (opcional)
        tipo: Tipo de usuario (admin, gerente, cliente, repartidor)
        estado: Estado del usuario (activo, inactivo, suspendido)
        fecha_creacion: Fecha de creación del usuario
        ultimo_acceso: Fecha del último acceso del usuario
    """
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True, comment="Identificador único del usuario")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="Correo electrónico del usuario")
    nombre = Column(String(100), nullable=False, comment="Nombre del usuario")
    apellido = Column(String(100), nullable=False, comment="Apellido del usuario")
    hashed_password = Column(String(200), nullable=False, comment="Contraseña hasheada")
    telefono = Column(String(20), nullable=True, comment="Número de teléfono")
    direccion = Column(String(200), nullable=True, comment="Dirección del usuario")
    tipo = Column(SQLEnum(TipoUsuario), default=TipoUsuario.CLIENTE, nullable=False, comment="Tipo de usuario")
    estado = Column(SQLEnum(EstadoUsuario), default=EstadoUsuario.ACTIVO, nullable=False, comment="Estado del usuario")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), comment="Fecha de creación del registro")
    ultimo_acceso = Column(DateTime(timezone=True), onupdate=func.now(), comment="Fecha del último acceso")
    
    # Relaciones
    locales = relationship("LocalDB", back_populates="gerente", cascade="all, delete-orphan", 
                         doc="Locales gestionados por este usuario (si es gerente)")
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, email='{self.email}', tipo='{self.tipo.value}', estado='{self.estado.value}')>"
    
    @property
    def nombre_completo(self) -> str:
        """Devuelve el nombre completo del usuario."""
        return f"{self.nombre} {self.apellido}"
