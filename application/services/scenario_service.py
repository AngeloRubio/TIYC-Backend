from typing import Dict, Any, Optional, List
from uuid import UUID

from domain.interfaces.services.scenario_extractor import ScenarioExtractorService
from domain.interfaces.repositories.scenario_repository import ScenarioRepository
from domain.entities.scenario import Scenario
from domain.entities.story import Story

class ScenarioService:
    """Servicio de aplicación para la gestión de escenarios."""
    
    def __init__(self, scenario_extractor: ScenarioExtractorService, scenario_repository: ScenarioRepository):
        self.scenario_extractor = scenario_extractor
        self.scenario_repository = scenario_repository
    # tenemos la pedagogia tradicional como predefinida
    def extract_scenarios(self, story, num_scenarios: int = 6, pedagogical_approach: str = "traditional") -> List[Dict[str, Any]]:
        """
        Extrae escenarios clave de un cuento para su ilustración.
        """
        # Extraer escenarios utilizando el servicio de extracción
        scenarios_data = self.scenario_extractor.extract_scenarios(
            title=story.title,
            content=story.content,
            num_scenarios=num_scenarios,
            pedagogical_approach=pedagogical_approach 
        )
        
        if not scenarios_data:
            return []
        
        saved_scenarios = []
        
        # Crear y guardar cada escenario
        for scenario_data in scenarios_data:
            scenario = Scenario(
                story_id=story.id,
                description=scenario_data["description"],
                sequence_number=scenario_data["sequence_number"],
                prompt_for_image=scenario_data["prompt_for_image"]
            )
            
            try:
                # Guardar el escenario en el repositorio
                scenario_id = self.scenario_repository.create(scenario)
                saved_scenarios.append(scenario.to_dict())
            except Exception as e:
                print(f"Error al guardar el escenario: {e}")
        
        return saved_scenarios
    
    def get_scenarios_by_story(self, story_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los escenarios asociados a un cuento.
        """
        try:
            scenarios = self.scenario_repository.get_by_story_id(UUID(story_id))
            return [scenario.to_dict() for scenario in scenarios]
        except Exception as e:
            print(f"Error al obtener los escenarios del cuento: {e}")
            return []
    
    def get_scenario_by_id(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un escenario por su ID.
        """
        try:
            scenario = self.scenario_repository.get_by_id(UUID(scenario_id))
            
            if not scenario:
                return None
                
            return scenario.to_dict()
        except Exception as e:
            print(f"Error al obtener el escenario: {e}")
            return None
