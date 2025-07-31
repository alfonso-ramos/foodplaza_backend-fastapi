"""
Core package for the application.

This package contains core functionality such as security, configuration, and utilities.
"""

from .config import settings

# Importación diferida para evitar dependencias circulares
# Las importaciones de seguridad se realizan en tiempo de ejecución cuando sea necesario

def __getattr__(name):
    if name in {
        'oauth2_scheme',
        'get_password_hash',
        'verify_password',
        'create_access_token',
        'get_current_user',
        'get_current_active_user',
    }:
        from . import security
        return getattr(security, name)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    'settings',
    'oauth2_scheme',
    'get_password_hash',
    'verify_password',
    'create_access_token',
    'get_current_user',
    'get_current_active_user',
]
