# Importar todos los modelos para que sean detectados por SQLAlchemy
from .base import Base
from .imagenes import ImagenDB
from .plazas import PlazaDB
from .locales import LocalDB
from .usuarios import UsuarioDB, TipoUsuario
from .menus import MenuDB
from .productos import ProductoDB

# Lista de todos los modelos para facilitar la importación
__all__ = [
    'Base',
    'ImagenDB',
    'PlazaDB',
    'LocalDB',
    'UsuarioDB',
    'TipoUsuario',
    'MenuDB',
    'ProductoDB',
]
