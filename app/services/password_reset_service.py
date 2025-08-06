import os
import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from dotenv import load_dotenv
from ..models import ResetCodeDB

# Cargar variables de entorno
load_dotenv()

class PasswordResetService:
    def __init__(self, db: Session):
        self.db = db
        self.code_expire_minutes = int(os.getenv("PASSWORD_RESET_CODE_EXPIRE_MINUTES", 15))
        self.code_length = int(os.getenv("PASSWORD_RESET_CODE_LENGTH", 6))
    
    def generate_verification_code(self) -> str:
        """Genera un código de verificación numérico"""
        return ''.join(random.choices(string.digits, k=self.code_length))
    
    def create_reset_code(self, email: str) -> ResetCodeDB:
        """
        Crea un nuevo código de restablecimiento para el correo electrónico proporcionado.
        Si ya existe un código sin usar para este correo, lo invalida.
        """
        # Invalidar códigos existentes para este correo
        self.db.query(ResetCodeDB).filter(
            ResetCodeDB.email == email,
            ResetCodeDB.used == False
        ).update({"used": True})
        self.db.commit()
        
        # Crear nuevo código
        expires_at = datetime.utcnow() + timedelta(minutes=self.code_expire_minutes)
        new_code = ResetCodeDB(
            email=email,
            code=self.generate_verification_code(),
            expires_at=expires_at,
            used=False
        )
        
        self.db.add(new_code)
        self.db.commit()
        self.db.refresh(new_code)
        
        return new_code
    
    def verify_reset_code(self, email: str, code: str) -> bool:
        """
        Verifica si el código de restablecimiento es válido para el correo electrónico dado.
        Un código es válido si:
        1. Existe en la base de datos
        2. No ha sido usado
        3. No ha expirado
        4. Corresponde al correo electrónico
        """
        current_time = datetime.utcnow()
        
        reset_code = self.db.query(ResetCodeDB).filter(
            ResetCodeDB.email == email,
            ResetCodeDB.code == code,
            ResetCodeDB.used == False,
            ResetCodeDB.expires_at > current_time
        ).first()
        
        if not reset_code:
            return False
            
        # Marcar el código como usado
        reset_code.used = True
        self.db.commit()
        
        return True
    
    def is_valid_reset_code(self, email: str, code: str) -> bool:
        """
        Verifica si el código de restablecimiento es válido sin marcarlo como usado.
        Útil para validar antes de permitir el cambio de contraseña.
        """
        current_time = datetime.utcnow()
        
        reset_code = self.db.query(ResetCodeDB).filter(
            ResetCodeDB.email == email,
            ResetCodeDB.code == code,
            ResetCodeDB.used == False,
            ResetCodeDB.expires_at > current_time
        ).first()
        
        return reset_code is not None
