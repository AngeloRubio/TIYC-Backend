from typing import Dict, Any, Optional
import bcrypt
from uuid import UUID

from domain.interfaces.services.auth_service import AuthService
from domain.interfaces.repositories.teacher_repository import TeacherRepository
from domain.entities.teacher import Teacher

class AuthenticationService:
    """Servicio de aplicación para autenticación del profesor."""
    
    def __init__(self, auth_service: AuthService, teacher_repository: TeacherRepository):
        self.auth_service = auth_service
        self.teacher_repository = teacher_repository
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Inicia sesión de un profesor."""
        return self.auth_service.login(email, password)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verifica un token  con JWT."""
        return self.auth_service.verify_token(token)
    
    def register(self, username: str, email: str, password: str, school: Optional[str] = None, grade: Optional[str] = None) -> Dict[str, Any]:
        """
        Registra un nuevo profesor.
        
        Returns-espectativa:
            {
                "success": True/False,
                "teacher": {teacher_data},
                "error": "Mensaje de error en caso de fallo"
            }
        """
        try:
            # Verificar si ya existe un profesor con el mismo email
            existing_teacher = self.teacher_repository.get_by_email(email)
            if existing_teacher:
                return {
                    "success": False,
                    "error": "El email ya está registrado"
                }
            
            # Generar hash de la contraseña
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Crear entidad del profesor (solo para el registro x consola)
            teacher = Teacher(
                username=username,
                email=email,
                password_hash=password_hash,
                school=school,
                grade=grade
            )
            
            # Guardar en el repositorio
            teacher_id = self.teacher_repository.create(teacher)
            
            return {
                "success": True,
                "teacher": teacher.to_dict(exclude=["password_hash"])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al registrar profesor: {str(e)}"
            }
    
    def get_teacher_by_id(self, teacher_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un profesor por su ID."""
        try:
            teacher = self.teacher_repository.get_by_id(UUID(teacher_id))
            
            if not teacher:
                return None
                
            return teacher.to_dict(exclude=["password_hash"])
        except Exception as e:
            print(f"Error al obtener el profesor: {e}")
            return None
    
    def update_profile(self, teacher_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza el perfil de un profesor.
        
        Returns - expectativa:
            {
                "success": True/False,
                "teacher": {teacher_data},
                "error": "Mensaje de error en caso de fallo"
            }
        """
        try:
            # Obtener el profesor actual
            teacher = self.teacher_repository.get_by_id(UUID(teacher_id))
            
            if not teacher:
                return {
                    "success": False,
                    "error": "Profesor no encontrado"
                }
            
            # Actualizar campos permitidos del usuario (profesor en este caso)
            if "username" in data:
                teacher.username = data["username"]
            if "school" in data:
                teacher.school = data["school"]
            if "grade" in data:
                teacher.grade = data["grade"]
            
            # Si se incluye nueva contraseña, actualizarla
            if "password" in data and data["password"]:
                teacher.password_hash = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Guardar cambios
            success = self.teacher_repository.update(teacher)
            
            if not success:
                return {
                    "success": False,
                    "error": "Error al actualizar el perfil"
                }
            
            return {
                "success": True,
                "teacher": teacher.to_dict(exclude=["password_hash"])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al actualizar perfil: {str(e)}"
            }