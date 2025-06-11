from abc import ABC, abstractmethod
from typing import Dict, Any

class ImageGeneratorService(ABC):
    """Interfaz para el servicio de generación de imágenes."""
    
    @abstractmethod
    def generate_image(
        self, 
        prompt: str,
        style: str = "children_illustration",
        width: int = 512,
        height: int = 512
    ) -> Dict[str, Any]:
        """
        Genera una imagen basada en el prompt proporcionado.
        
        Args:
            prompt: Descripción detallada para la generación de la imagen.
            style: Estilo artístico para la imagen.
            width: Ancho de la imagen en píxeles.
            height: Alto de la imagen en píxeles.
            
        Returns:
            Diccionario con información de la imagen generada.
            {
                "success": True/False,
                "image_url": "ruta/a/la/imagen.png",
                "error": "Mensaje de error en caso de fallo"
            }
        """
        pass