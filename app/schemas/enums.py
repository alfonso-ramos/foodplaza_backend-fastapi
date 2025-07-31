from enum import Enum

class TipoUsuario(str, Enum):
    """Enumeración para los tipos de usuario en el sistema."""
    ADMIN = "admin"
    GERENTE = "gerente"
    CLIENTE = "cliente"
    REPARTIDOR = "repartidor"

class EstadoUsuario(str, Enum):
    """Enumeración para los estados de un usuario."""
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"
