from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.scenario import Scenario

class ScenarioRepository(ABC):
    """Interfaz para el repositorio de escenarios."""
    
    @abstractmethod
    def create(self, scenario: Scenario) -> UUID:
        """Crea un nuevo escenario en el repositorio."""
        pass
    
    @abstractmethod
    def get_by_id(self, scenario_id: UUID) -> Optional[Scenario]:
        """Obtiene un escenario por su ID."""
        pass
    
    @abstractmethod
    def get_by_story_id(self, story_id: UUID) -> List[Scenario]:
        """Obtiene todos los escenarios asociados a un cuento."""
        pass
    
    @abstractmethod
    def update(self, scenario: Scenario) -> bool:
        """Actualiza un escenario existente."""
        pass
    
    @abstractmethod
    def delete(self, scenario_id: UUID) -> bool:
        """Elimina un escenario por su ID."""
        pass
    
    @abstractmethod
    def delete_by_story_id(self, story_id: UUID) -> bool:
        """Elimina todos los escenarios asociados a un cuento."""
        pass