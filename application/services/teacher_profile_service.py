from typing import Dict, Any, Optional
from uuid import UUID
import bcrypt

from domain.interfaces.repositories.teacher_repository import TeacherRepository
from domain.entities.teacher import Teacher
from domain.exceptions.domain_exceptions import EntityNotFoundException, ValidationException

class TeacherProfileService:
    """Servicio de aplicación para gestión de perfiles de profesores."""
    
    def __init__(self, teacher_repository: TeacherRepository):
        self.teacher_repository = teacher_repository
    
    def get_profile(self, teacher_id: str) -> Dict[str, Any]:
        """
        Obtiene el perfil completo de un profesor.
        
        Returns:
            {
                "success": True/False,
                "profile": {teacher_data},
                "error": "Mensaje de error en caso de fallo"
            }
        """
        try:
            teacher = self.teacher_repository.get_by_id(UUID(teacher_id))
            
            if not teacher:
                return {
                    "success": False,
                    "error": "Profesor no encontrado"
                }
            
            return {
                "success": True,
                "profile": teacher.to_dict(exclude=["password_hash"])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener perfil: {str(e)}"
            }
    
    def update_profile(self, teacher_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza el perfil de un profesor.
        
        Args:
            teacher_id: ID del profesor
            update_data: Datos a actualizar
            
        Returns:
            {
                "success": True/False,
                "profile": {teacher_data},
                "message": "Mensaje de éxito",
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
            
            # Validar que hay campos para actualizar
            if not update_data:
                return {
                    "success": False,
                    "error": "No se proporcionaron datos para actualizar"
                }
            
            # Validaciones específicas
            validation_errors = self._validate_update_data(update_data, teacher.id)
            if validation_errors:
                return {
                    "success": False,
                    "error": "Errores de validación",
                    "validation_errors": validation_errors
                }
            
            # Actualizar campos permitidos
            if "username" in update_data:
                teacher.username = update_data["username"]
            if "school" in update_data:
                teacher.school = update_data["school"]
            if "grade" in update_data:
                teacher.grade = update_data["grade"]
            
            # Guardar cambios
            success = self.teacher_repository.update(teacher)
            
            if not success:
                return {
                    "success": False,
                    "error": "Error al actualizar el perfil en la base de datos"
                }
            
            return {
                "success": True,
                "profile": teacher.to_dict(exclude=["password_hash"]),
                "message": "Perfil actualizado exitosamente"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error interno al actualizar perfil: {str(e)}"
            }
    
    def change_password(self, teacher_id: str, password_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cambia la contraseña de un profesor.
        
        Args:
            teacher_id: ID del profesor
            password_data: Datos de contraseña (current_password, new_password)
            
        Returns:
            {
                "success": True/False,
                "message": "Mensaje de éxito",
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
            
            current_password = password_data.get("current_password")
            new_password = password_data.get("new_password")
            
            # Verificar contraseña actual
            if not bcrypt.checkpw(current_password.encode('utf-8'), teacher.password_hash.encode('utf-8')):
                return {
                    "success": False,
                    "error": "La contraseña actual es incorrecta"
                }
            
            # Generar hash de la nueva contraseña
            new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            teacher.password_hash = new_password_hash
            
            # Guardar cambios
            success = self.teacher_repository.update(teacher)
            
            if not success:
                return {
                    "success": False,
                    "error": "Error al actualizar la contraseña en la base de datos"
                }
            
            return {
                "success": True,
                "message": "Contraseña cambiada exitosamente"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error interno al cambiar contraseña: {str(e)}"
            }
    
    def get_activity_summary(self, teacher_id: str) -> Dict[str, Any]:
        """
        Obtiene un resumen de la actividad del profesor.
        
        Returns:
            {
                "success": True/False,
                "summary": {activity_data},
                "error": "Mensaje de error en caso de fallo"
            }
        """
        try:
            teacher = self.teacher_repository.get_by_id(UUID(teacher_id))
            
            if not teacher:
                return {
                    "success": False,
                    "error": "Profesor no encontrado"
                }
            
            # TODO: Implementar lógica real de estadísticas
            # Por ahora retornamos datos mock
            summary = {
                "total_stories": 10,
                "stories_this_month": 3,
                "favorite_category": "Aventura",
                "favorite_approach": "traditional",
                "last_story_date": "2025-01-15",
                "stories_by_month": {
                    "2024-11": 2,
                    "2024-12": 5,
                    "2025-01": 3
                },
                "stories_by_category": {
                    "Aventura": 4,
                    "Ciencia": 3,
                    "Fantasía": 3
                }
            }
            
            return {
                "success": True,
                "summary": summary
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener resumen de actividad: {str(e)}"
            }
    
    def _validate_update_data(self, update_data: Dict[str, Any], teacher_id: UUID) -> list:
        """Valida los datos de actualización."""
        errors = []
        
        # Validar username único si se está actualizando
        if "username" in update_data:
            username = update_data["username"]
            # Aquí podrías agregar validación de username único
            # existing_teacher = self.teacher_repository.get_by_username(username)
            # if existing_teacher and existing_teacher.id != teacher_id:
            #     errors.append("El nombre de usuario ya está en uso")
        
        return errors