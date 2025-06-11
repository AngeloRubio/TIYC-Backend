from flask import Blueprint, request, jsonify
from typing import Dict, Any
import json
import datetime
import traceback
from uuid import UUID

from application.services.story_service import StoryService
from application.services.scenario_service import ScenarioService
from application.services.image_service import ImageService
from application.services.illustration_orchestrator import IllustrationOrchestratorService
from application.dtos.request_dtos import GenerateStoryRequest
from domain.exceptions.domain_exceptions import DomainException
from domain.entities.story import Story
from domain.entities.scenario import Scenario
from domain.entities.image import Image

story_routes = Blueprint('story_routes', __name__)

# La inyección de dependencias se realizará en el archivo principal
story_service = None
scenario_service = None
image_service = None
illustration_orchestrator_service = None

def init_routes(story_svc, illustration_orchestrator_svc, scenario_svc=None, image_svc=None):
    """Inicializa los servicios necesarios para las rutas."""
    global story_service, illustration_orchestrator_service, scenario_service, image_service
    story_service = story_svc
    illustration_orchestrator_service = illustration_orchestrator_svc
    scenario_service = scenario_svc
    image_service = image_svc

@story_routes.route('/generate-illustrated-story', methods=['POST'])
def generate_illustrated_story():
    """
    Genera un cuento ilustrado completo siguiendo el flujo de tres pasos.
    GUARDA EN BASE DE DATOS - Este es el flujo original.
    """
    try:
        # Log inicial
        print("------ INICIO DE GENERACIÓN DE CUENTO ILUSTRADO (CON GUARDADO) ------")
        print(f"Timestamp: {datetime.datetime.now().isoformat()}")
        
        # Log de datos recibidos
        print("Recibiendo solicitud POST...")
        data = request.json
        print(f"Datos recibidos: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # Validar los datos de entrada
        print("Validando datos de entrada...")
        if not data:
            print("ERROR: No se recibieron datos JSON")
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos JSON'
            }), 400
            
        if 'context' not in data:
            print("ERROR: Falta el campo 'context'")
            return jsonify({
                'success': False,
                'error': 'Se requiere el campo context'
            }), 400
            
        if 'category' not in data:
            print("ERROR: Falta el campo 'category'")
            return jsonify({
                'success': False,
                'error': 'Se requiere el campo category'
            }), 400
        
        # Validar el enfoque pedagógico
        print("Validando enfoque pedagógico...")
        pedagogical_approach = data.get('pedagogical_approach', 'traditional')
        print(f"Enfoque pedagógico recibido: {pedagogical_approach}")
        
        if pedagogical_approach not in ['montessori', 'waldorf', 'traditional']:
            print(f"ERROR: Enfoque pedagógico no válido: {pedagogical_approach}")
            return jsonify({
                'success': False,
                'error': 'Enfoque pedagógico no válido. Opciones: montessori, waldorf, traditional'
            }), 400
        
        # Crear el DTO de solicitud
        print("Creando DTO de solicitud...")
        try:
            story_request = GenerateStoryRequest(
                context=data['context'],
                category=data['category'],
                pedagogical_approach=pedagogical_approach,
                teacher_id=data.get('teacher_id'),
                target_age=data.get('target_age'),
                max_length=data.get('max_length'),
                num_illustrations=data.get('num_illustrations', 6)
            )
            print(f"DTO creado correctamente")
        except Exception as dto_error:
            print(f"ERROR al crear DTO: {str(dto_error)}")
            import traceback
            print("Traceback de error en DTO:")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': f'Error al crear DTO: {str(dto_error)}'
            }), 400
        
        # Usar illustration_orchestrator_service con save_to_db=True (comportamiento original)
        print("Llamando al orquestador de ilustraciones (CON GUARDADO)...")
        try:
            # Verificar si el servicio está inicializado
            print(f"¿illustration_orchestrator_service inicializado? {illustration_orchestrator_service is not None}")
            
            if not illustration_orchestrator_service:
                print("ERROR: illustration_orchestrator_service no inicializado")
                return jsonify({
                    'success': False,
                    'error': 'Servicio orquestador no inicializado'
                }), 500
            
            # Generar el cuento ilustrado completo usando el orquestador CON GUARDADO
            result = illustration_orchestrator_service.create_illustrated_story(
                request=story_request, 
                save_to_db=True  # ⭐ COMPORTAMIENTO ORIGINAL: GUARDAR EN BD
            )
            print(f"Resultado de generación: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if not result.get('success', False):
                print(f"ERROR reportado por orquestador: {result.get('error', 'Error desconocido')}")
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Error al generar el cuento ilustrado'),
                    'step': result.get('step', 'unknown')
                }), 500
            
            print("------ ÉXITO EN GENERACIÓN DE CUENTO ILUSTRADO (GUARDADO) ------")
            return jsonify(result), 200
            
        except Exception as service_error:
            print(f"ERROR al llamar al orquestrador: {str(service_error)}")
            import traceback
            print("Traceback de error en orquestador:")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': f'Error en orquestador: {str(service_error)}'
            }), 500
        
    except Exception as e:
        # Capturar y registrar cualquier excepción no manejada
        print(f"ERROR GENERAL NO MANEJADO: {str(e)}")
        import traceback
        print("Traceback completo:")
        traceback.print_exc()
        
        # Incluir información sobre el tipo de excepción
        error_type = type(e).__name__
        print(f"Tipo de excepción: {error_type}")
        
        return jsonify({
            'success': False,
            'error': f"{error_type}: {str(e)}"
        }), 500

@story_routes.route('/preview-illustrated-story', methods=['POST'])
def preview_illustrated_story():
    """
    🆕 NUEVO ENDPOINT: Genera un cuento ilustrado completo para PREVIEW.
    
    Esta función es idéntica a generate_illustrated_story() pero con una diferencia clave:
    - NO GUARDA EN BASE DE DATOS (save_to_db=False)
    - Retorna datos temporales que el frontend puede mostrar inmediatamente
    - Permite al usuario ver el resultado antes de decidir si lo guarda
    
    Este endpoint es crucial para el flujo de UX del proyecto TIYC donde los usuarios
    pueden generar múltiples versiones y solo guardar la que más les guste.
    """
    try:
        # Log inicial con indicador de PREVIEW
        print("------ INICIO DE GENERACIÓN DE CUENTO ILUSTRADO (PREVIEW MODE) ------")
        print(f"Timestamp: {datetime.datetime.now().isoformat()}")
        print("⭐ MODO PREVIEW: No se guardará en base de datos")
        
        # Log de datos recibidos
        print("Recibiendo solicitud POST para preview...")
        data = request.json
        print(f"Datos recibidos: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # Validar los datos de entrada (misma validación que el endpoint original)
        print("Validando datos de entrada...")
        if not data:
            print("ERROR: No se recibieron datos JSON")
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos JSON'
            }), 400
            
        if 'context' not in data:
            print("ERROR: Falta el campo 'context'")
            return jsonify({
                'success': False,
                'error': 'Se requiere el campo context'
            }), 400
            
        if 'category' not in data:
            print("ERROR: Falta el campo 'category'")
            return jsonify({
                'success': False,
                'error': 'Se requiere el campo category'
            }), 400
        
        # Validar el enfoque pedagógico
        print("Validando enfoque pedagógico...")
        pedagogical_approach = data.get('pedagogical_approach', 'traditional')
        print(f"Enfoque pedagógico recibido: {pedagogical_approach}")
        
        if pedagogical_approach not in ['montessori', 'waldorf', 'traditional']:
            print(f"ERROR: Enfoque pedagógico no válido: {pedagogical_approach}")
            return jsonify({
                'success': False,
                'error': 'Enfoque pedagógico no válido. Opciones: montessori, waldorf, traditional'
            }), 400
        
        # Crear el DTO de solicitud (idéntico al endpoint original)
        print("Creando DTO de solicitud para preview...")
        try:
            story_request = GenerateStoryRequest(
                context=data['context'],
                category=data['category'],
                pedagogical_approach=pedagogical_approach,
                teacher_id=data.get('teacher_id'),
                target_age=data.get('target_age'),
                max_length=data.get('max_length'),
                num_illustrations=data.get('num_illustrations', 6)
            )
            print(f"DTO creado correctamente para preview")
        except Exception as dto_error:
            print(f"ERROR al crear DTO: {str(dto_error)}")
            import traceback
            print("Traceback de error en DTO:")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': f'Error al crear DTO: {str(dto_error)}'
            }), 400
        
        # ⭐ DIFERENCIA CLAVE: Usar save_to_db=False para modo preview
        print("Llamando al orquestador de ilustraciones (MODO PREVIEW)...")
        try:
            # Verificar si el servicio está inicializado
            print(f"¿illustration_orchestrator_service inicializado? {illustration_orchestrator_service is not None}")
            
            if not illustration_orchestrator_service:
                print("ERROR: illustration_orchestrator_service no inicializado")
                return jsonify({
                    'success': False,
                    'error': 'Servicio orquestador no inicializado'
                }), 500
            
            # 🎯 LÍNEA CLAVE: Generar en modo preview (sin guardar en BD)
            result = illustration_orchestrator_service.create_illustrated_story(
                request=story_request, 
                save_to_db=False  # ⭐ DIFERENCIA CRÍTICA: NO GUARDAR EN BD
            )
            
            print(f"Resultado de generación preview: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if not result.get('success', False):
                print(f"ERROR reportado por orquestador en preview: {result.get('error', 'Error desconocido')}")
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Error al generar el cuento preview'),
                    'step': result.get('step', 'unknown')
                }), 500
            
            # Agregar metadata específica del preview
            result['preview_info'] = {
                'generated_at': datetime.datetime.now().isoformat(),
                'is_preview': True,
                'can_save': True,  # Indicar que este contenido puede ser guardado posteriormente
                'expires_info': 'Este preview es temporal. Guárdalo en tu biblioteca para conservarlo.'
            }
            
            print("------ ÉXITO EN GENERACIÓN DE CUENTO PREVIEW ------")
            print(f"✅ Preview generado con {len(result.get('scenarios', []))} escenarios y {len(result.get('images', []))} imágenes")
            
            return jsonify(result), 200
            
        except Exception as service_error:
            print(f"ERROR al llamar al orquestrador en preview: {str(service_error)}")
            import traceback
            print("Traceback de error en orquestador preview:")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': f'Error en orquestador preview: {str(service_error)}'
            }), 500
        
    except Exception as e:
        # Capturar y registrar cualquier excepción no manejada
        print(f"ERROR GENERAL NO MANEJADO EN PREVIEW: {str(e)}")
        import traceback
        print("Traceback completo preview:")
        traceback.print_exc()
        
        # Incluir información sobre el tipo de excepción
        error_type = type(e).__name__
        print(f"Tipo de excepción en preview: {error_type}")
        
        return jsonify({
            'success': False,
            'error': f"Preview {error_type}: {str(e)}"
        }), 500

@story_routes.route('/save-previewed-story', methods=['POST'])
def save_previewed_story():
    """
    Guarda un cuento previewed en la base de datos.
    Recibe el JSON completo del preview y lo persiste usando los repositorios existentes.
    """
    try:
        data = request.json
        
        # Validación básica
        if not data or not data.get('story') or not data.get('scenarios'):
            return jsonify({
                'success': False,
                'error': 'Se requiere story, scenarios en el JSON'
            }), 400
        
        # Verificar que sea un preview válido
        if data.get('mode') != 'preview':
            return jsonify({
                'success': False,
                'error': 'Solo se pueden guardar datos de preview'
            }), 400
        
        # Guardar usando el orquestador pero solo la parte de persistencia
        result = _save_preview_to_database(data)
        
        if not result.get('success', False):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Error al guardar el cuento')
            }), 500
        
        return jsonify({
            'success': True,
            'story_id': result['story_id'],
            'message': 'Cuento guardado exitosamente en tu biblioteca'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al guardar: {str(e)}'
        }), 500

@story_routes.route('/regenerate-scenario-image/<scenario_id>', methods=['POST'])
def regenerate_scenario_image(scenario_id):
    """
    Regenera la imagen de un escenario específico usando el mismo prompt.
    Útil para cuando el usuario quiere una versión diferente de la imagen.
    """
    try:
        data = request.json or {}
        
        # Verificar que los servicios estén inicializados
        if not scenario_service or not image_service:
            return jsonify({
                'success': False,
                'error': 'Servicios no inicializados correctamente'
            }), 500
        
        # Obtener el escenario para conseguir el prompt original
        scenario = scenario_service.get_scenario_by_id(scenario_id)
        
        if not scenario:
            return jsonify({
                'success': False,
                'error': 'Escenario no encontrado'
            }), 404
        
        # Obtener pedagogical_approach del request o usar default
        pedagogical_approach = data.get('pedagogical_approach', 'traditional')
        
        # Crear request para nueva imagen
        from application.dtos.request_dtos import GenerateImageRequest
        image_request = GenerateImageRequest(
            prompt=scenario['prompt_for_image'],
            pedagogical_approach=pedagogical_approach,
            style=data.get('style', 'children_illustration'),
            width=data.get('width', 512),
            height=data.get('height', 512)
        )
        
        # Generar nueva imagen - esto reemplazará la imagen existente
        result = image_service.generate_image(scenario_id, image_request)
        
        if not result.get('success', False):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Error al regenerar imagen')
            }), 500
        
        return jsonify({
            'success': True,
            'new_image': result['image'],
            'message': 'Nueva imagen generada exitosamente'
        }), 200
        
    except Exception as e:
        print(f"ERROR en regenerate_scenario_image: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error al regenerar imagen: {str(e)}'
        }), 500

def _save_preview_to_database(preview_data):
    """
    Función auxiliar que toma datos de preview y los persiste en BD.
    Reutiliza todos los repositorios existentes.
    """
    try:
        # Acceder a los servicios a través del orquestador
        scenario_svc = illustration_orchestrator_service.scenario_service
        image_svc = illustration_orchestrator_service.image_service
        
        # 1. Guardar el Story
        story_data = preview_data['story']
        story = Story(
            title=story_data['title'],
            content=story_data['content'],
            context=story_data['context'],
            category=story_data['category'],
            pedagogical_approach=story_data['pedagogical_approach'],
            teacher_id=UUID(story_data['teacher_id']) if story_data.get('teacher_id') else None,
            created_at=datetime.datetime.now()
        )
        
        story_id = story_service.story_repository.create(story)
        
        # 2. Guardar los Scenarios
        scenarios_data = preview_data['scenarios']
        scenario_mapping = {}  # mapeo de IDs temporales a IDs reales
        
        for scenario_data in scenarios_data:
            scenario = Scenario(
                story_id=story_id,
                description=scenario_data['description'],
                sequence_number=scenario_data['sequence_number'],
                prompt_for_image=scenario_data['prompt_for_image'],
                created_at=datetime.datetime.now()
            )
            
            real_scenario_id = scenario_svc.scenario_repository.create(scenario)
            scenario_mapping[scenario_data['id']] = str(real_scenario_id)
        
        # 3. Guardar las Images usando el mapeo de scenario IDs
        images_data = preview_data.get('images', [])
        
        for image_data in images_data:
            temp_scenario_id = image_data['scenario_id']
            real_scenario_id = scenario_mapping.get(temp_scenario_id)
            
            if real_scenario_id:
                image = Image(
                    scenario_id=UUID(real_scenario_id),
                    prompt=image_data['prompt'],
                    image_url=image_data['image_url'],
                    created_at=datetime.datetime.now()
                )
                
                image_svc.image_repository.create(image)
        
        return {
            'success': True,
            'story_id': str(story_id)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error en persistencia: {str(e)}'
        }

# Los demás endpoints existentes permanecen sin cambios
@story_routes.route('/stories/<story_id>', methods=['GET'])
def get_story(story_id):
    """
    Obtiene un cuento por su ID.
    """
    try:
        print(f"📖 Obteniendo cuento: {story_id}")
        
        if not story_service:
            return jsonify({
                'success': False,
                'error': 'Servicio de cuentos no inicializado'
            }), 500
        
        story = story_service.get_story_by_id(story_id)
        
        if not story:
            return jsonify({
                'success': False,
                'error': 'Cuento no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'story': story
        }), 200
        
    except Exception as e:
        print(f"ERROR al obtener cuento: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@story_routes.route('/illustrated-stories/<story_id>', methods=['GET'])
def get_illustrated_story(story_id):
    """
    Obtiene un cuento ilustrado completo por su ID.
    """
    try:
        print(f"🎨 Obteniendo cuento ilustrado: {story_id}")
        
        if not illustration_orchestrator_service:
            return jsonify({
                'success': False,
                'error': 'Servicio orquestador no inicializado'
            }), 500
        
        result = illustration_orchestrator_service.get_illustrated_story(story_id)
        
        if not result.get('success', False):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Cuento no encontrado')
            }), 404 if 'no encontrado' in result.get('error', '').lower() else 500
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"ERROR al obtener cuento ilustrado: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@story_routes.route('/stories/recent', methods=['GET'])
def get_recent_stories():
    """
    Obtiene los cuentos más recientes.
    """
    try:
        print("📚 Obteniendo cuentos recientes")
        
        if not story_service:
            return jsonify({
                'success': False,
                'error': 'Servicio de cuentos no inicializado'
            }), 500
        
        limit = request.args.get('limit', default=10, type=int)
        stories = story_service.get_recent_stories(limit)
        
        return jsonify({
            'success': True,
            'stories': stories
        }), 200
        
    except Exception as e:
        print(f"ERROR al obtener cuentos recientes: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@story_routes.route('/stories/teacher/<teacher_id>', methods=['GET'])
def get_teacher_stories(teacher_id):
    """
    Obtiene los cuentos creados por un profesor específico.
    """
    try:
        print(f"👨‍🏫 Obteniendo cuentos del profesor: {teacher_id}")
        
        if not story_service:
            return jsonify({
                'success': False,
                'error': 'Servicio de cuentos no inicializado'
            }), 500
        
        limit = request.args.get('limit', default=10, type=int)
        stories = story_service.get_stories_by_teacher(teacher_id, limit)
        
        return jsonify({
            'success': True,
            'stories': stories
        }), 200
        
    except Exception as e:
        print(f"ERROR al obtener cuentos del profesor: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500