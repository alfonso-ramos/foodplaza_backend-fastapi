# This file makes the app directory a Python package
from .db import Base, engine, get_db, create_tables
from . import models, schemas

# Crea las tablas en la base de datos
create_tables()

__all__ = [
    'Base',
    'engine',
    'get_db',
    'models',
    'schemas',
    'create_tables'
]