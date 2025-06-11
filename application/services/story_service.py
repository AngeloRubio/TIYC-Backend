from typing import Dict, Any, Optional, List
from uuid import UUID

from domain.interfaces.services.story_generator import StoryGeneratorService
from domain.interfaces.repositories.story_repository import StoryRepository
from domain.entities.story import Story
from application.dtos.request_dtos import GenerateStoryRequest
from application.dtos.response_dtos import StoryResponse

class StoryService:
    """Servicio de aplicación para la gestión de cuentos."""
    
    def __init__(self, story_generator: StoryGeneratorService, story_repository: StoryRepository):
        self.story_generator = story_generator
        self.story_repository = story_repository
    
    def generate_story(self, request: GenerateStoryRequest) -> Dict[str, Any]:
        """
        Genera un cuento basado en los parámetros proporcionados.
        """
        try:
            print(f"📝 Generando cuento con enfoque: {request.pedagogical_approach}")
            
            # CORRECCIÓN: Pasar todos los parámetros necesarios incluyendo pedagogical_approach
            result = self.story_generator.generate_story(
                context=request.context,
                category=request.category,
                pedagogical_approach=request.pedagogical_approach,  # ✅ Agregado
                target_age=request.target_age,
                max_length=request.max_length
            )
            
            if not result.get("success", False):
                print(f"❌ Error en generador: {result.get('error')}")
                return {
                    "success": False,
                    "error": result.get("error", "Error desconocido al generar el cuento")
                }
            
            print(f"✅ Cuento generado: {result.get('title', 'Sin título')}")
            
            # Crear la entidad de cuento
            story = Story(
                title=result["title"],
                content=result["content"],
                context=request.context,
                category=request.category,
                pedagogical_approach=request.pedagogical_approach,  # ✅ Incluido
                teacher_id=UUID(request.teacher_id) if request.teacher_id else None
            )
            
            # Guardar el cuento en el repositorio
            try:
                print(f"💾 Guardando cuento en base de datos...")
                story_id = self.story_repository.create(story)
                print(f"✅ Cuento guardado con ID: {story_id}")
                
                # Preparar la respuesta
                return {
                    "success": True,
                    "story": story.to_dict()
                }
            except Exception as e:
                print(f"❌ Error al guardar cuento: {str(e)}")
                import traceback
                traceback.print_exc()
                return {
                    "success": False,
                    "error": f"Error al guardar el cuento: {str(e)}"
                }
                
        except Exception as e:
            print(f"❌ Error general en story_service: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Error interno en generación de cuento: {str(e)}"
            }
    
    def get_story_by_id(self, story_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un cuento por su ID.
        """
        try:
            print(f"🔍 Buscando cuento con ID: {story_id}")
            story = self.story_repository.get_by_id(UUID(story_id))
            
            if not story:
                print(f"❌ Cuento no encontrado: {story_id}")
                return None
                
            print(f"✅ Cuento encontrado: {story.title}")
            return story.to_dict()
        except Exception as e:
            print(f"❌ Error al obtener el cuento: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_recent_stories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene los cuentos más recientes.
        """
        try:
            print(f"📚 Obteniendo {limit} cuentos recientes")
            stories = self.story_repository.get_recent(limit)
            result = [story.to_dict() for story in stories]
            print(f"✅ Se encontraron {len(result)} cuentos")
            return result
        except Exception as e:
            print(f"❌ Error al obtener los cuentos recientes: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_stories_by_teacher(self, teacher_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene los cuentos creados por un profesor específico.
        """
        try:
            print(f"👨‍🏫 Obteniendo cuentos del profesor {teacher_id} (límite: {limit})")
            stories = self.story_repository.get_by_teacher_id(UUID(teacher_id), limit)
            result = [story.to_dict() for story in stories]
            print(f"✅ Se encontraron {len(result)} cuentos del profesor")
            return result
        except Exception as e:
            print(f"❌ Error al obtener los cuentos del profesor: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def delete_story(self, story_id: str) -> bool:
        """
        Elimina un cuento por su ID.
        """
        try:
            print(f"🗑️ Eliminando cuento: {story_id}")
            result = self.story_repository.delete(UUID(story_id))
            if result:
                print(f"✅ Cuento eliminado exitosamente")
            else:
                print(f"❌ No se pudo eliminar el cuento")
            return result
        except Exception as e:
            print(f"❌ Error al eliminar el cuento: {e}")
            import traceback
            traceback.print_exc()
            return False