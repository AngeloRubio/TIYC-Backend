from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import jwt
import logging

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuración y componentes
from config import DB_CONFIG, IMAGE_STORAGE_PATH, GEMINI_API_KEY, STABILITY_API_KEY, JWT_SECRET_KEY
from domain.exceptions.domain_exceptions import DomainException

# Importar implementaciones de repositorios
from infrastructure.repositories.mysql_story_repository import MySQLStoryRepository
from infrastructure.repositories.mysql_scenario_repository import MySQLScenarioRepository
from infrastructure.repositories.mysql_image_repository import MySQLImageRepository
from infrastructure.repositories.mysql_teacher_repository import MySQLTeacherRepository

# Importar implementaciones de servicios
from infrastructure.services.gemini_story_generator import GeminiStoryGenerator
from infrastructure.services.gemini_scenario_extractor import GeminiScenarioExtractor
from infrastructure.services.stability_ai_image_generator import StabilityAIImageGenerator
from infrastructure.services.jwt_auth_service import JWTAuthService

# Importar servicios de aplicación
from application.services.story_service import StoryService
from application.services.scenario_service import ScenarioService
from application.services.image_service import ImageService
from application.services.illustration_orchestrator import IllustrationOrchestratorService
from application.services.auth_service import AuthenticationService

# Importar rutas
from presentation.api.story_routes import story_routes, init_routes as init_story_routes
from presentation.api.image_routes import image_routes, init_routes as init_image_routes
from presentation.api.auth_routes import auth_routes, init_routes as init_auth_routes

# Configuración de logging
from utils.logging_config import configure_logging

# Logger para este módulo
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configurar logging
configure_logging(app)

# Configurar manejador de errores global
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, DomainException):
        return jsonify({
            'success': False,
            'error': str(e),
            'type': e.__class__.__name__
        }), 400
    
    app.logger.error(f"Error no manejado: {e}")
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500

# Inicializar repositorios
story_repository = MySQLStoryRepository()
scenario_repository = MySQLScenarioRepository()
image_repository = MySQLImageRepository()
teacher_repository = MySQLTeacherRepository()

# Inicializar servicios de dominio
story_generator = GeminiStoryGenerator(GEMINI_API_KEY)
scenario_extractor = GeminiScenarioExtractor(GEMINI_API_KEY)
image_generator = StabilityAIImageGenerator(STABILITY_API_KEY, IMAGE_STORAGE_PATH)
jwt_auth_service = JWTAuthService(teacher_repository)

# Inicializar servicios de aplicación
story_service = StoryService(story_generator, story_repository)
scenario_service = ScenarioService(scenario_extractor, scenario_repository)
image_service = ImageService(image_generator, image_repository)
illustration_orchestrator = IllustrationOrchestratorService(
    story_service, scenario_service, image_service
)
auth_service = AuthenticationService(jwt_auth_service, teacher_repository)

# Inicializar rutas con sus respectivos servicios
init_story_routes(story_service, illustration_orchestrator, scenario_service, image_service)
init_image_routes(image_service, IMAGE_STORAGE_PATH, story_service, scenario_service)
init_auth_routes(auth_service)

# Registrar blueprints
app.register_blueprint(story_routes, url_prefix='/api')
app.register_blueprint(image_routes, url_prefix='/api')
app.register_blueprint(auth_routes, url_prefix='/api/auth')

# Exponer el servicio de autenticación globalmente
app.auth_service = auth_service

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_STORAGE_PATH, filename)

@app.route('/')
def index():
    return jsonify({
        'status': 'online',
        'message': 'API de generación de cuentos ilustrados',
        'version': '1.0.0'
    })

# Punto de entrada principal
if __name__ == '__main__':
    # Crear directorios necesarios
    os.makedirs(IMAGE_STORAGE_PATH, exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Verificar configuración crítica
    if not JWT_SECRET_KEY:
        logger.warning("JWT_SECRET_KEY no configurada. Se usará una clave predeterminada.")
    
    # Mostrar configuración al iniciar
    logger.info("Iniciando aplicación TIYC")
    print(f"=== Configuración actual ===")
    print(f"Directorio de imágenes: {IMAGE_STORAGE_PATH}")
    print(f"Gemini API Key configurada: {'Sí' if GEMINI_API_KEY else 'No'}")
    print(f"Stability API Key configurada: {'Sí' if STABILITY_API_KEY else 'No'}")
    print(f"JWT Secret Key configurada: {'Sí' if JWT_SECRET_KEY else 'No'}")
    print(f"Base de datos: {DB_CONFIG['database']} en {DB_CONFIG['host']}")
    print(f"===========================")
    print(f"Servidor iniciado en http://localhost:5000")
    
    # Iniciar aplicación
    app.run(debug=True)