from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AuthService(ABC):
    """Interfaz para el servicio de autenticación."""
    
    @abstractmethod
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Autentica a un profesor con email y contraseña.
        
        Returns:
            {
                "success": True/False,
                "token": "jwt_token",
                "teacher": {teacher_data},
                "error": "Mensaje de error en caso de fallo"
            }
        """
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica la validez de un token.
        
        Returns:
            {
                "valid": True/False,
                "teacher_id": "id del profesor si el token es válido",
                "error": "Mensaje de error en caso de fallo"
            }
        """
        pass