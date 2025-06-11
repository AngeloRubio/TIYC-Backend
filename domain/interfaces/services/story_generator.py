from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class StoryGeneratorService(ABC):
    """Interfaz para el servicio de generación de cuentos."""
    
    @abstractmethod
    def generate_story(
        self, 
        context: str, 
        category: str,
        target_age: Optional[str] = None,
        max_length: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Genera un cuento basado en el contexto y la categoría proporcionados.
        
        Args:
            context: Descripción o contexto para la generación del cuento.
            category: Categoría o género del cuento (aventura, fantasía, etc.)
            target_age: Edad objetivo para el cuento (opcional)
            max_length: Longitud máxima del cuento en palabras (opcional)
            
        Returns:
            Diccionario con el título y contenido del cuento generado.
            {
                "title": "Título del cuento",
                "content": "Contenido completo del cuento..."
            }
        """
        pass