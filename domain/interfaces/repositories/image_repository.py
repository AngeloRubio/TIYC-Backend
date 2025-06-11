from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.image import Image

class ImageRepository(ABC):
    """Interfaz para el repositorio de imágenes."""
    
    @abstractmethod
    def create(self, image: Image) -> UUID:
        """Crea una nueva imagen en el repositorio."""
        pass
    
    @abstractmethod
    def get_by_id(self, image_id: UUID) -> Optional[Image]:
        """Obtiene una imagen por su ID."""
        pass
    
    @abstractmethod
    def get_by_scenario_id(self, scenario_id: UUID) -> Optional[Image]:
        """Obtiene una imagen asociada a un escenario específico."""
        pass
    
    @abstractmethod
    def get_by_story_id(self, story_id: UUID) -> List[Image]:
        """Obtiene todas las imágenes asociadas a un cuento."""
        pass
    
    @abstractmethod
    def update(self, image: Image) -> bool:
        """Actualiza una imagen existente."""
        pass
    
    @abstractmethod
    def delete(self, image_id: UUID) -> bool:
        """Elimina una imagen por su ID."""
        pass
    
    @abstractmethod
    def delete_by_scenario_id(self, scenario_id: UUID) -> bool:
        """Elimina todas las imágenes asociadas a un escenario."""
        pass