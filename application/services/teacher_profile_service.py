# application/services/teacher_profile_service.py

from typing import Dict, Any, Optional, List
from uuid import UUID
import bcrypt
from datetime import datetime

from domain.interfaces.repositories.teacher_repository import TeacherRepository
from domain.entities.teacher import Teacher
from domain.exceptions.domain_exceptions import (
    ValidationException, 
    EntityNotFoundException,
    DomainException
)
from application.dtos.request_dtos import UpdateProfileRequest, ChangePasswordRequest
from application.dtos.response_dtos import ProfileResponse


class TeacherProfileService:
    """Servicio de aplicación para gestión de perfiles de profesores."""
    
    def __init__(self, teacher_repository: TeacherRepository):
        self._teacher_repository = teacher_repository
        self._validators = self._initialize_validators()
    
    def get_profile(self, teacher_id: str) -> Dict[str, Any]:
        try:
            teacher = self._get_teacher_or_fail(teacher_id)
            
            profile = ProfileResponse(
                id=str(teacher.id),
                username=teacher.username,
                email=teacher.email,
                school=teacher.school,
                grade=teacher.grade,
                created_at=teacher.created_at.isoformat(),
                profile_completion=self._calculate_profile_completion(teacher),
                story_count=self._get_teacher_story_count(teacher_id),
                last_activity=self._get_last_activity(teacher_id)
            )
            
            return {
                "success": True,
                "profile": profile.to_dict()
            }
            
        except EntityNotFoundException as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"Error interno: {str(e)}"}
    
    def update_profile(self, teacher_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            validation_result = self._validate_profile_update(update_data)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": "Datos inválidos",
                    "validation_errors": validation_result["errors"]
                }
            
            teacher = self._get_teacher_or_fail(teacher_id)
            
            commands = self._build_update_commands(teacher, update_data)
            for command in commands:
                command.execute()
            
            success = self._teacher_repository.update(teacher)
            
            if not success:
                return {"success": False, "error": "Error al guardar cambios"}
            
            return {
                "success": True,
                "profile": teacher.to_dict(exclude=["password_hash"]),
                "message": "Perfil actualizado exitosamente"
            }
            
        except EntityNotFoundException as e:
            return {"success": False, "error": str(e)}
        except ValidationException as e:
            return {"success": False, "error": str(e), "validation_errors": e.errors}
        except Exception as e:
            return {"success": False, "error": f"Error interno: {str(e)}"}
    
    def change_password(self, teacher_id: str, password_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            teacher = self._get_teacher_or_fail(teacher_id)
            
            if not self._verify_current_password(teacher, password_data.get("current_password")):
                return {"success": False, "error": "Contraseña actual incorrecta"}
            
            new_password = password_data.get("new_password")
            confirm_password = password_data.get("confirm_password")
            
            password_validation = self._validate_new_password(new_password, confirm_password)
            if not password_validation["valid"]:
                return {
                    "success": False,
                    "error": "Contraseña inválida",
                    "validation_errors": password_validation["errors"]
                }
            
            teacher.password_hash = self._hash_password(new_password)
            
            success = self._teacher_repository.update(teacher)
            
            if not success:
                return {"success": False, "error": "Error al cambiar contraseña"}
            
            return {
                "success": True,
                "message": "Contraseña cambiada exitosamente"
            }
            
        except EntityNotFoundException as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"Error interno: {str(e)}"}
    
    def get_activity_summary(self, teacher_id: str) -> Dict[str, Any]:
        try:
            teacher = self._get_teacher_or_fail(teacher_id)
            
            summary = {
                "total_stories": self._get_teacher_story_count(teacher_id),
                "stories_this_month": self._get_stories_count_by_period(teacher_id, "month"),
                "stories_this_week": self._get_stories_count_by_period(teacher_id, "week"),
                "favorite_category": self._get_favorite_category(teacher_id),
                "favorite_pedagogical_approach": self._get_favorite_approach(teacher_id),
                "profile_completion": self._calculate_profile_completion(teacher)
            }
            
            return {"success": True, "summary": summary}
            
        except EntityNotFoundException as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"Error interno: {str(e)}"}
    
    def _get_teacher_or_fail(self, teacher_id: str) -> Teacher:
        teacher = self._teacher_repository.get_by_id(UUID(teacher_id))
        if not teacher:
            raise EntityNotFoundException("Teacher", teacher_id)
        return teacher
    
    def _validate_profile_update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        errors = []
        
        for field, validators in self._validators.items():
            if field in data:
                value = data[field]
                for validator in validators:
                    if not validator.validate(value):
                        errors.append(validator.get_error_message())
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def _initialize_validators(self) -> Dict[str, List]:
        return {
            "username": [
                LengthValidator(min_length=3, max_length=50, field="username"),
                AlphanumericValidator(field="username")
            ],
            "school": [
                LengthValidator(min_length=3, max_length=100, field="school")
            ],
            "grade": [
                GradeValidator()
            ]
        }
    
    def _build_update_commands(self, teacher: Teacher, data: Dict[str, Any]) -> List:
        commands = []
        
        if "username" in data:
            commands.append(UpdateUsernameCommand(teacher, data["username"]))
        if "school" in data:
            commands.append(UpdateSchoolCommand(teacher, data["school"]))
        if "grade" in data:
            commands.append(UpdateGradeCommand(teacher, data["grade"]))
        
        return commands
    
    def _calculate_profile_completion(self, teacher: Teacher) -> int:
        fields = [teacher.username, teacher.email, teacher.school, teacher.grade]
        completed_fields = sum(1 for field in fields if field and field.strip())
        return int((completed_fields / len(fields)) * 100)
    
    def _verify_current_password(self, teacher: Teacher, current_password: str) -> bool:
        if not current_password:
            return False
        return bcrypt.checkpw(
            current_password.encode('utf-8'), 
            teacher.password_hash.encode('utf-8')
        )
    
    def _validate_new_password(self, new_password: str, confirm_password: str) -> Dict[str, Any]:
        errors = []
        
        if not new_password:
            errors.append("La nueva contraseña es requerida")
        elif len(new_password) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres")
        elif new_password != confirm_password:
            errors.append("Las contraseñas no coinciden")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _get_teacher_story_count(self, teacher_id: str) -> int:
        return 0
    
    def _get_stories_count_by_period(self, teacher_id: str, period: str) -> int:
        return 0
    
    def _get_favorite_category(self, teacher_id: str) -> Optional[str]:
        return None
    
    def _get_favorite_approach(self, teacher_id: str) -> Optional[str]:
        return None
    
    def _get_last_activity(self, teacher_id: str) -> Optional[str]:
        return None


class UpdateCommand:
    def execute(self):
        raise NotImplementedError


class UpdateUsernameCommand(UpdateCommand):
    def __init__(self, teacher: Teacher, new_username: str):
        self.teacher = teacher
        self.new_username = new_username
    
    def execute(self):
        self.teacher.username = self.new_username


class UpdateSchoolCommand(UpdateCommand):
    def __init__(self, teacher: Teacher, new_school: str):
        self.teacher = teacher
        self.new_school = new_school
    
    def execute(self):
        self.teacher.school = self.new_school


class UpdateGradeCommand(UpdateCommand):
    def __init__(self, teacher: Teacher, new_grade: str):
        self.teacher = teacher
        self.new_grade = new_grade
    
    def execute(self):
        self.teacher.grade = self.new_grade


class Validator:
    def validate(self, value: Any) -> bool:
        raise NotImplementedError
    
    def get_error_message(self) -> str:
        raise NotImplementedError


class LengthValidator(Validator):
    def __init__(self, min_length: int, max_length: int, field: str):
        self.min_length = min_length
        self.max_length = max_length
        self.field = field
    
    def validate(self, value: str) -> bool:
        if not value:
            return False
        return self.min_length <= len(value.strip()) <= self.max_length
    
    def get_error_message(self) -> str:
        return f"{self.field} debe tener entre {self.min_length} y {self.max_length} caracteres"


class AlphanumericValidator(Validator):
    def __init__(self, field: str):
        self.field = field
    
    def validate(self, value: str) -> bool:
        return value and value.replace(" ", "").replace("_", "").isalnum()
    
    def get_error_message(self) -> str:
        return f"{self.field} solo puede contener letras, números, espacios y guiones bajos"


class GradeValidator(Validator):
    VALID_GRADES = [
        "Primero de Básica", "Segundo de Básica", "Tercero de Básica",
        "Cuarto de Básica", "Quinto de Básica", "Sexto de Básica",
        "Séptimo de Básica"
    ]
    
    def validate(self, value: str) -> bool:
        return value in self.VALID_GRADES
    
    def get_error_message(self) -> str:
        return "Grado escolar no válido"