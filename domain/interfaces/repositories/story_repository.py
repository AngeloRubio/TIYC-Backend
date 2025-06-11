from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.story import Story

class StoryRepository(ABC):
    """Interfaz para el repositorio de cuentos."""
    
    @abstractmethod
    def create(self, story: Story) -> UUID:
        """Crea un nuevo cuento en el repositorio."""
        pass
    
    @abstractmethod
    def get_by_id(self, story_id: UUID) -> Optional[Story]:
        """Obtiene un cuento por su ID."""
        pass
    
    @abstractmethod
    def get_by_teacher_id(self, teacher_id: UUID, limit: int = 10) -> List[Story]:
        """Obtiene los cuentos creados por un profesor específico."""
        pass
    
    @abstractmethod
    def get_recent(self, limit: int = 10) -> List[Story]:
        """Obtiene los cuentos más recientes."""
        pass
    
    @abstractmethod
    def update(self, story: Story) -> bool:
        """Actualiza un cuento existente."""
        pass
    
    @abstractmethod
    def delete(self, story_id: UUID) -> bool:
        """Elimina un cuento por su ID."""
        pass