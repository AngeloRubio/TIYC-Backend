from typing import Dict, Any, List
from uuid import UUID

from domain.entities.story import Story
from application.dtos.request_dtos import GenerateStoryRequest, GenerateImageRequest
from application.services.story_service import StoryService
from application.services.scenario_service import ScenarioService
from application.services.image_service import ImageService

class IllustrationOrchestratorService:
    """
    Servicio orquestador que coordina el flujo completo de generación de cuentos ilustrados:
    1. Generar cuento
    2. Extraer escenarios clave
    3. Generar imágenes para cada escenario
    
    NUEVA FUNCIONALIDAD: Soporte para modo preview sin persistencia
    """
    
    def __init__(
        self,
        story_service: StoryService,
        scenario_service: ScenarioService,
        image_service: ImageService
    ):
        self.story_service = story_service
        self.scenario_service = scenario_service
        self.image_service = image_service

    def create_illustrated_story(self, request: GenerateStoryRequest, save_to_db: bool = True) -> Dict[str, Any]:
        """
        Crea un cuento ilustrado completo siguiendo el flujo de tres pasos.
        
        Args:
            request: Datos para generar el cuento
            save_to_db: Si True, persiste en BD. Si False, solo genera contenido temporal
        
        Returns:
            Dict con story, scenarios, images y metadata
        """
        try:
            print(f"🚀 Iniciando generación de cuento ilustrado (save_to_db={save_to_db})")
            
            # Paso 1: Generar el cuento
            print(f"📝 Paso 1: Generando cuento...")
            
            if save_to_db:
                # Flujo normal: guardar en BD
                story_result = self.story_service.generate_story(request)
                
                if not story_result.get("success", False):
                    print(f"❌ Error en generación de cuento: {story_result.get('error')}")
                    return {
                        "success": False,
                        "error": story_result.get("error", "Error al generar el cuento"),
                        "step": "story_generation"
                    }
                
                story_data = story_result["story"]
                story = Story.from_dict(story_data)
                
            else:
                # Flujo preview: generar sin guardar
                story_result = self._generate_story_preview(request)
                
                if not story_result.get("success", False):
                    print(f"❌ Error en generación de cuento preview: {story_result.get('error')}")
                    return {
                        "success": False,
                        "error": story_result.get("error", "Error al generar el cuento"),
                        "step": "story_generation"
                    }
                
                # Crear entidad temporal sin ID de BD
                story = Story(
                    title=story_result["title"],
                    content=story_result["content"],
                    context=request.context,
                    category=request.category,
                    pedagogical_approach=request.pedagogical_approach,
                    teacher_id=UUID(request.teacher_id) if request.teacher_id else None
                )
                story_data = story.to_dict()
            
            print(f"✅ Cuento generado: {story.title}")
            
            # Paso 2: Extraer escenarios clave del cuento
            print(f"🎬 Paso 2: Extrayendo escenarios...")
            num_illustrations = request.num_illustrations or 6
            
            if save_to_db:
                # Flujo normal: guardar escenarios en BD
                scenarios = self.scenario_service.extract_scenarios(
                    story=story,
                    num_scenarios=num_illustrations,
                    pedagogical_approach=request.pedagogical_approach
                )
            else:
                # Flujo preview: generar escenarios temporales
                scenarios = self._extract_scenarios_preview(
                    story=story,
                    num_scenarios=num_illustrations,
                    pedagogical_approach=request.pedagogical_approach
                )
            
            if not scenarios:
                print(f"❌ No se pudieron extraer escenarios")
                return {
                    "success": False,
                    "error": "No se pudieron extraer escenarios del cuento",
                    "step": "scenario_extraction",
                    "story": story_data
                }
            
            print(f"✅ Se extrajeron {len(scenarios)} escenarios")
            
            # Paso 3: Generar imágenes para cada escenario
            print(f"🎨 Paso 3: Generando imágenes...")
            images = []
            for i, scenario in enumerate(scenarios):
                print(f"🖼️ Generando imagen {i+1}/{len(scenarios)}")
                
                if save_to_db:
                    # Flujo normal: guardar imagen en BD
                    image_request = GenerateImageRequest(
                        prompt=scenario["prompt_for_image"],
                        pedagogical_approach=request.pedagogical_approach,
                        style="children_illustration"
                    )
                    
                    image_result = self.image_service.generate_image(
                        scenario_id=scenario["id"],
                        request=image_request
                    )
                    
                    if image_result.get("success", False):
                        images.append(image_result["image"])
                        print(f"✅ Imagen {i+1} generada exitosamente")
                    else:
                        print(f"⚠️ Error al generar imagen {i+1}: {image_result.get('error')}")
                else:
                    # Flujo preview: generar imagen temporal
                    image_result = self._generate_image_preview(
                        scenario_id=scenario["id"],
                        prompt=scenario["prompt_for_image"],
                        pedagogical_approach=request.pedagogical_approach
                    )
                    
                    if image_result.get("success", False):
                        images.append(image_result["image"])
                        print(f"✅ Imagen {i+1} generada exitosamente (preview)")
                    else:
                        print(f"⚠️ Error al generar imagen {i+1}: {image_result.get('error')}")
            
            print(f"🎉 Proceso completado: {len(images)} imágenes generadas")
            
            # Construir respuesta
            response = {
                "success": True,
                "story": story_data,
                "scenarios": scenarios,
                "images": images,
                "summary": f"Cuento '{story.title}' generado con {len(scenarios)} escenarios y {len(images)} imágenes",
                "mode": "saved" if save_to_db else "preview"  # Indicar el modo usado
            }
            
            return response
            
        except Exception as e:
            print(f"💥 Error crítico en orchestrator: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Error interno en la generación: {str(e)}",
                "step": "orchestrator_error"
            }
    
    def _generate_story_preview(self, request: GenerateStoryRequest) -> Dict[str, Any]:
        """
        Genera un cuento usando el story_generator pero sin persistir en BD.
        
        Este método es clave para el flujo de preview, ya que reutiliza toda la lógica
        de generación existente pero evita la persistencia.
        """
        try:
            # Usar directamente el generador de cuentos sin pasar por story_service
            result = self.story_service.story_generator.generate_story(
                context=request.context,
                category=request.category,
                pedagogical_approach=request.pedagogical_approach,
                target_age=request.target_age,
                max_length=request.max_length
            )
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al generar cuento preview: {str(e)}"
            }
    
    def _extract_scenarios_preview(self, story: Story, num_scenarios: int, pedagogical_approach: str) -> List[Dict[str, Any]]:
        """
        Extrae escenarios temporales sin guardar en BD.
        
        Genera escenarios con IDs temporales que el frontend puede usar
        para referencias locales pero que no persisten en la base de datos.
        """
        try:
            from uuid import uuid4
            
            # Usar directamente el extractor de escenarios
            scenarios_data = self.scenario_service.scenario_extractor.extract_scenarios(
                title=story.title,
                content=story.content,
                num_scenarios=num_scenarios,
                pedagogical_approach=pedagogical_approach
            )
            
            if not scenarios_data:
                return []
            
            # Crear escenarios temporales con IDs únicos para referencias
            temp_scenarios = []
            for scenario_data in scenarios_data:
                temp_scenario = {
                    "id": str(uuid4()),  # ID temporal para referencias
                    "story_id": str(story.id),  # Referencia al story temporal
                    "description": scenario_data["description"],
                    "sequence_number": scenario_data["sequence_number"],
                    "prompt_for_image": scenario_data["prompt_for_image"],
                    "created_at": story.created_at.isoformat() if story.created_at else None,
                    "mode": "preview"  # Marcador para identificar que es temporal
                }
                temp_scenarios.append(temp_scenario)
            
            return temp_scenarios
            
        except Exception as e:
            print(f"Error al extraer escenarios preview: {e}")
            return []
    
    def _generate_image_preview(self, scenario_id: str, prompt: str, pedagogical_approach: str) -> Dict[str, Any]:
        """
        Genera una imagen temporal sin guardar en BD.
        
        Usa el generador de imágenes existente pero retorna datos temporales
        que el frontend puede mostrar sin persistencia.
        """
        try:
            from uuid import uuid4
            from datetime import datetime
            
            # Usar directamente el generador de imágenes
            result = self.image_service.image_generator.generate_image(
                prompt=prompt,
                pedagogical_approach=pedagogical_approach,
                style="children_illustration",
                width=512,
                height=512
            )
            
            if not result.get("success", False):
                return result
            
            # Crear estructura de imagen temporal
            temp_image = {
                "id": str(uuid4()),  # ID temporal
                "scenario_id": scenario_id,
                "prompt": prompt,
                "image_url": result["image_url"],
                "created_at": datetime.now().isoformat(),
                "mode": "preview"  # Marcador temporal
            }
            
            return {
                "success": True,
                "image": temp_image
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al generar imagen preview: {str(e)}"
            }

    # Método existente sin cambios para compatibilidad hacia atrás
    def get_illustrated_story(self, story_id: str) -> Dict[str, Any]:
        """
        Obtiene un cuento ilustrado completo por su ID.
        Este método no cambia - solo para cuentos ya guardados en BD.
        """
        try:
            print(f"📖 Obteniendo cuento ilustrado: {story_id}")
            
            # Obtener el cuento
            story_data = self.story_service.get_story_by_id(story_id)
            
            if not story_data:
                return {
                    "success": False,
                    "error": "Cuento no encontrado"
                }
            
            # Obtener los escenarios asociados al cuento
            scenarios = self.scenario_service.get_scenarios_by_story(story_id)
            
            # Obtener las imágenes asociadas a los escenarios
            images = self.image_service.get_images_by_story(story_id)
            
            # Asociar cada imagen con su escenario correspondiente
            scenario_images = {}
            for image in images:
                scenario_images[image["scenario_id"]] = image
            
            # Construir los escenarios con sus imágenes
            scenarios_with_images = []
            for scenario in scenarios:
                scenario_copy = scenario.copy()
                scenario_copy["image"] = scenario_images.get(scenario["id"])
                scenarios_with_images.append(scenario_copy)
            
            print(f"✅ Cuento ilustrado obtenido: {len(scenarios_with_images)} escenarios")
            
            # Preparar y retornar la respuesta completa
            return {
                "success": True,
                "story": story_data,
                "scenarios": scenarios_with_images,
                "mode": "saved"  # Indicar que viene de BD
            }
            
        except Exception as e:
            print(f"💥 Error al obtener cuento ilustrado: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Error al obtener el cuento ilustrado: {str(e)}"
            }