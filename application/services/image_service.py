from typing import Dict, Any, Optional, List
from uuid import UUID

from domain.interfaces.services.image_generator import ImageGeneratorService
from domain.interfaces.repositories.image_repository import ImageRepository
from domain.entities.image import Image
from application.dtos.request_dtos import GenerateImageRequest

class ImageService:
    """Servicio de aplicación para la gestión de imágenes."""
    
    def __init__(self, image_generator: ImageGeneratorService, image_repository: ImageRepository):
        self.image_generator = image_generator
        self.image_repository = image_repository
    
    def generate_image(self, scenario_id: str, request: GenerateImageRequest) -> Dict[str, Any]:
        """
        Genera una imagen para un escenario específico.
        """
        # Generar la imagen utilizando el servicio de generación
        result = self.image_generator.generate_image(
            prompt=request.prompt,
            style=request.style,
            width=request.width,
            height=request.height
        )
        
        if not result.get("success", False):
            return {
                "success": False,
                "error": result.get("error", "Error desconocido al generar la imagen")
            }
        
        # Crear la entidad de imagen
        image = Image(
            scenario_id=UUID(scenario_id),
            prompt=request.prompt,
            image_url=result["image_url"]
        )
        
        # Guardar la imagen en el repositorio
        try:
            image_id = self.image_repository.create(image)
            
            return {
                "success": True,
                "image": image.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al guardar la imagen: {str(e)}"
            }
    
    def get_image_by_id(self, image_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene una imagen por su ID.
        """
        try:
            image = self.image_repository.get_by_id(UUID(image_id))
            
            if not image:
                return None
                
            return image.to_dict()
        except Exception as e:
            print(f"Error al obtener la imagen: {e}")
            return None
    
    def get_image_by_scenario_id(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene una imagen por el ID de su escenario.
        """
        try:
            image = self.image_repository.get_by_scenario_id(UUID(scenario_id))
            
            if not image:
                return None
                
            return image.to_dict()
        except Exception as e:
            print(f"Error al obtener imagen por scenario: {e}")
            return None
    
    def get_images_by_story(self, story_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las imágenes asociadas a un cuento.
        """
        try:
            images = self.image_repository.get_by_story_id(UUID(story_id))
            return [image.to_dict() for image in images]
        except Exception as e:
            print(f"Error al obtener las imágenes del cuento: {e}")
            return []
    
    def delete_image(self, image_id: str) -> bool:
        """
        Elimina una imagen por su ID.
        """
        try:
            return self.image_repository.delete(UUID(image_id))
        except Exception as e:
            print(f"Error al eliminar la imagen: {e}")
            return False