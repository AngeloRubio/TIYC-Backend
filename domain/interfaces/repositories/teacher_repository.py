from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.teacher import Teacher  # Debemos crear esta entidad

class TeacherRepository(ABC):
    """Interfaz para el repositorio de profesores."""
    
    @abstractmethod
    def create(self, teacher: Teacher) -> UUID:
        """Crea un nuevo profesor en el repositorio."""
        pass
    
    @abstractmethod
    def get_by_id(self, teacher_id: UUID) -> Optional[Teacher]:
        """Obtiene un profesor por su ID."""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Teacher]:
        """Obtiene un profesor por su email."""
        pass
    
    @abstractmethod
    def update(self, teacher: Teacher) -> bool:
        """Actualiza un profesor existente."""
        pass
    
    @abstractmethod
    def delete(self, teacher_id: UUID) -> bool:
        """Elimina un profesor por su ID."""
        pass