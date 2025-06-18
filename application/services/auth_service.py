from typing import Dict, Any, Optional
import bcrypt
from uuid import UUID

from domain.interfaces.services.auth_service import AuthService
from domain.interfaces.repositories.teacher_repository import TeacherRepository
from domain.entities.teacher import Teacher

class AuthenticationService:
    
    def __init__(self, auth_service: AuthService, teacher_repository: TeacherRepository):
        self.auth_service = auth_service
        self.teacher_repository = teacher_repository
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        return self.auth_service.login(email, password)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self.auth_service.verify_token(token)
    
    def register(self, username: str, email: str, password: str, school: Optional[str] = None, grade: Optional[str] = None) -> Dict[str, Any]:
        try:
            existing_teacher = self.teacher_repository.get_by_email(email)
            if existing_teacher:
                return {"success": False, "error": "El email ya está registrado"}
            
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            teacher = Teacher(
                username=username,
                email=email,
                password_hash=password_hash,
                school=school,
                grade=grade
            )
            
            teacher_id = self.teacher_repository.create(teacher)
            
            return {
                "success": True,
                "teacher": teacher.to_dict(exclude=["password_hash"])
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error al registrar profesor: {str(e)}"}
    
    def get_teacher_by_id(self, teacher_id: str) -> Optional[Dict[str, Any]]:
        try:
            teacher = self.teacher_repository.get_by_id(UUID(teacher_id))
            if not teacher:
                return None
            return teacher.to_dict(exclude=["password_hash"])
        except Exception as e:
            print(f"Error al obtener el profesor: {e}")
            return None
    
    def update_profile(self, teacher_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            teacher = self.teacher_repository.get_by_id(UUID(teacher_id))
            
            if not teacher:
                return {"success": False, "error": "Profesor no encontrado"}
            
            if "username" in data:
                teacher.username = data["username"]
            if "school" in data:
                teacher.school = data["school"]
            if "grade" in data:
                teacher.grade = data["grade"]
            
            if "password" in data and data["password"]:
                teacher.password_hash = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            success = self.teacher_repository.update(teacher)
            
            if not success:
                return {"success": False, "error": "Error al actualizar el perfil"}
            
            return {
                "success": True,
                "teacher": teacher.to_dict(exclude=["password_hash"])
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error al actualizar perfil: {str(e)}"}