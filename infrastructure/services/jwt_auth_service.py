import jwt
import datetime
import os
import bcrypt
from typing import Dict, Any, Optional

from domain.interfaces.services.auth_service import AuthService
from domain.interfaces.repositories.teacher_repository import TeacherRepository
from domain.exceptions.domain_exceptions import ValidationException

class JWTAuthService(AuthService):
    """Implementación del servicio de autenticación usando JWT."""
    
    def __init__(self, teacher_repository: TeacherRepository):
        self.teacher_repository = teacher_repository
        self.secret_key = os.getenv("JWT_SECRET_KEY", "default_secret_key")
        self.token_expiration = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Autentica a un profesor y genera un token JWT."""
        try:
            # Buscar al profesor por email
            teacher = self.teacher_repository.get_by_email(email)
            
            if not teacher:
                return {
                    "success": False,
                    "error": "Email o contraseña incorrectos"
                }
            
            # Verificar la contraseña
            if not bcrypt.checkpw(password.encode('utf-8'), teacher.password_hash.encode('utf-8')):
                return {
                    "success": False,
                    "error": "Email o contraseña incorrectos"
                }
            
            # Generar el token JWT
            payload = {
                "teacher_id": str(teacher.id),
                "email": teacher.email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=self.token_expiration)
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm="HS256")
            
            return {
                "success": True,
                "token": token,
                "teacher": teacher.to_dict(exclude=["password_hash"])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error de autenticación: {str(e)}"
            }
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verifica si un token JWT es válido."""
        try:
            # Decodificar el token
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # Verificar si el profesor existe
            teacher_id = payload.get("teacher_id")
            teacher = self.teacher_repository.get_by_id(teacher_id)
            
            if not teacher:
                return {
                    "valid": False,
                    "error": "Profesor no encontrado"
                }
            
            return {
                "valid": True,
                "teacher_id": teacher_id
            }
            
        except jwt.ExpiredSignatureError:
            return {
                "valid": False,
                "error": "Token expirado"
            }
        except jwt.InvalidTokenError:
            return {
                "valid": False,
                "error": "Token inválido"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Error al verificar token: {str(e)}"
            }