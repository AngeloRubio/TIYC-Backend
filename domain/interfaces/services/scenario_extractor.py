from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ScenarioExtractorService(ABC):
    """Interfaz para el servicio de extracción de escenarios clave de un cuento."""
    
    @abstractmethod
    def extract_scenarios(
        self, 
        title: str, 
        content: str, 
        num_scenarios: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Extrae los escenarios clave de un cuento para su generacion.
        
        Args:
            title: Título del cuento.
            content: Contenido completo del cuento.
            num_scenarios: Número de escenarios a extraer.
            
        Returns:
            Lista de escenarios con su descripción y prompt para generación de imagen.
            [
                {
                    "sequence_number": 1,
                    "description": "Descripción del escenario",
                    "prompt_for_image": "Prompt optimizado para generar la imagen"
                },
                ...
            ]
        """
        pass
