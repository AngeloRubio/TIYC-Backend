
from flask import jsonify
from functools import wraps

from domain.exceptions.domain_exceptions import (
    DomainException,
    EntityNotFoundException,
    ValidationException,
    StoryGenerationException,
    ScenarioExtractionException,
    ImageGenerationException,
    RepositoryException,
    ExternalServiceException
)

def error_handler(f):
    """
    Decorador para manejar excepciones de manera consistente en las rutas de la API.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except EntityNotFoundException as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'error_type': 'not_found'
            }), 404
        except ValidationException as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'error_type': 'validation_error',
                'errors': e.errors
            }), 400
        except StoryGenerationException as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'error_type': 'story_generation_error'
            }), 500
        except ScenarioExtractionException as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'error_type': 'scenario_extraction_error'
            }), 500
        except ImageGenerationException as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'error_type': 'image_generation_error'
            }), 500
        except RepositoryException as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'error_type': 'repository_error'
            }), 500
        except ExternalServiceException as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'error_type': 'external_service_error',
                'service': e.service_name
            }), 503
        except DomainException as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'error_type': 'domain_error'
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Error interno del servidor',
                'error_type': 'server_error'
            }), 500
    return decorated


