
from dataclasses import dataclass
from typing import Optional, List

@dataclass(frozen=True)
class StoryGenerationParameters:
    """
    Parámetros inmutables para la generación de cuentos.
    """
    context: str
    category: str
    target_age: Optional[str] = None
    max_length: Optional[int] = None
    
    def __post_init__(self):
        """Validación de los parámetros."""
        if not self.context:
            raise ValueError("El contexto no puede estar vacío")
        
        if not self.category:
            raise ValueError("La categoría no puede estar vacía")
        
        if self.max_length is not None and self.max_length <= 0:
            raise ValueError("La longitud máxima debe ser un número positivo")


@dataclass(frozen=True)
class ScenarioExtractionParameters:
    """
    Parámetros inmutables para la extracción de escenarios.
    """
    title: str
    content: str
    num_scenarios: int = 6
    
    def __post_init__(self):
        """Validación de los parámetros."""
        if not self.title:
            raise ValueError("El título no puede estar vacío")
        
        if not self.content:
            raise ValueError("El contenido no puede estar vacío")
        
        if self.num_scenarios <= 0:
            raise ValueError("El número de escenarios debe ser un número positivo")


@dataclass(frozen=True)
class ImageGenerationParameters:
    """
    Parámetros inmutables para la generación de imágenes.
    """
    prompt: str
    style: str = "children_illustration"
    width: int = 512
    height: int = 512
    
    def __post_init__(self):
        """Validación de los parámetros."""
        if not self.prompt:
            raise ValueError("El prompt no puede estar vacío")
        
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Las dimensiones deben ser números positivos")