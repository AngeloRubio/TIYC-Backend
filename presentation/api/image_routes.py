from flask import Blueprint, request, jsonify, send_from_directory
import os
import uuid

from application.services.image_service import ImageService
from application.dtos.request_dtos import GenerateImageRequest
from application.services.scenario_service import ScenarioService
from application.services.story_service import StoryService
from domain.entities.story import Story
from domain.exceptions.domain_exceptions import DomainException

image_routes = Blueprint('image_routes', __name__)

image_service = None
image_storage_path = None
story_service = None
scenario_service = None

def init_routes(image_svc, storage_path, story_svc=None, scenario_svc=None):
    """Inicializa los servicios necesarios para las rutas."""
    global image_service, image_storage_path, story_service, scenario_service
    image_service = image_svc
    image_storage_path = storage_path
    story_service = story_svc
    scenario_service = scenario_svc

@image_routes.route('/generate-image', methods=['POST'])
def generate_image():
    """
    Genera una imagen basada en el prompt proporcionado.
    """
    try:
        data = request.json
        
        # Validar los datos de entrada
        if not data or 'prompt' not in data or 'scenario_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Se requieren prompt y scenario_id'
            }), 400
        
        # Crear el DTO de solicitud
        image_request = GenerateImageRequest(
            prompt=data['prompt'],
            pedagogical_approach=data.get('pedagogical_approach', 'traditional'),
            style=data.get('style', 'children_illustration'),
            width=data.get('width', 512),
            height=data.get('height', 512)
        )
        
        # Generar la imagen
        result = image_service.generate_image(data['scenario_id'], image_request)
        
        if not result.get('success', False):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Error al generar la imagen')
            }), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@image_routes.route('/generate-scenarios-and-images/<story_id>', methods=['POST'])
def generate_scenarios_and_images(story_id):
    """
    Extrae escenarios y genera imágenes para un cuento existente.
    """
    try:
        print(f"\n====== GENERANDO ESCENARIOS E IMÁGENES PARA CUENTO {story_id} ======")
        
        # Verificar que los servicios necesarios estén disponibles
        if not story_service or not scenario_service:
            return jsonify({
                'success': False,
                'error': 'Servicios no inicializados correctamente'
            }), 500
        
        # Obtener cuento
        story_data = story_service.get_story_by_id(story_id)
        if not story_data:
            return jsonify({
                'success': False,
                'error': f'Cuento con ID {story_id} no encontrado'
            }), 404
        
        print(f"Cuento encontrado: {story_data['title']}")
        print(f"Enfoque pedagógico: {story_data.get('pedagogical_approach', 'traditional')}")
        
        # Crear entidad Story
        from domain.entities.story import Story
        story = Story.from_dict(story_data)
        
        # Datos de solicitud - manejo más seguro
        try:
            if request.is_json and request.get_data(as_text=True).strip():
                data = request.get_json()
            else:
                data = {}
        except Exception as e:
            print(f"Error al procesar JSON: {e}")
            data = {}
            
        num_scenarios = int(data.get('num_scenarios', 4))
        print(f"Número de escenarios a generar: {num_scenarios}")
        
        # Extraer escenarios
        print(f"Extrayendo {num_scenarios} escenarios...")
        
        # Aquí verificamos si el método acepta pedagogical_approach
        try:
            scenarios = scenario_service.extract_scenarios(
                story=story,
                num_scenarios=num_scenarios
            )
        except Exception as e:
            print(f"Error al extraer escenarios: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': f'Error al extraer escenarios: {str(e)}'
            }), 500
        
        if not scenarios:
            return jsonify({
                'success': False,
                'error': 'No se pudieron extraer escenarios del cuento'
            }), 500
        
        print(f"Se extrajeron {len(scenarios)} escenarios")
        
        # Generar imágenes para cada escenario
        images = []
        for idx, scenario in enumerate(scenarios):
            print(f"\nGenerando imagen {idx+1}/{len(scenarios)} para escenario {scenario['id']}")
            prompt = scenario.get('prompt_for_image', '')
            print(f"Prompt: {prompt[:100]}...")
            
            image_request = GenerateImageRequest(
                prompt=prompt,
                style="children_illustration"
            )
            
            try:
                result = image_service.generate_image(
                    scenario_id=scenario["id"],
                    request=image_request
                )
                
                if result.get('success', False):
                    print(f"Imagen generada correctamente: {result.get('image_url')}")
                    images.append(result["image"])
                else:
                    print(f"Error al generar imagen: {result.get('error')}")
            except Exception as e:
                print(f"Excepción al generar imagen: {str(e)}")
                import traceback
                traceback.print_exc()
        
        # Preparar respuesta
        return jsonify({
            'success': True,
            'story': story_data,
            'scenarios': scenarios,
            'images': images,
            'summary': f"Se generaron {len(images)} imágenes de {len(scenarios)} escenarios"
        }), 200
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    

@image_routes.route('/images/<image_id>', methods=['GET'])
def get_image(image_id):
    """
    Obtiene una imagen por su ID.
    """
    try:
        image = image_service.get_image_by_id(image_id)
        
        if not image:
            return jsonify({
                'success': False,
                'error': 'Imagen no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'image': image
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@image_routes.route('/images/story/<story_id>', methods=['GET'])
def get_story_images(story_id):
    """
    Obtiene todas las imágenes asociadas a un cuento.
    """
    try:
        images = image_service.get_images_by_story(story_id)
        
        return jsonify({
            'success': True,
            'images': images
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@image_routes.route('/static/images/<path:filename>')
def serve_image(filename):
    """
    Sirve una imagen estática desde el sistema de archivos.
    """
    try:
        return send_from_directory(image_storage_path, filename)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al cargar la imagen: {str(e)}'
        }), 404