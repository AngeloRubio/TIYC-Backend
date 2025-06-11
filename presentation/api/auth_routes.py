from flask import Blueprint, request, jsonify
import json

from application.services.auth_service import AuthenticationService

auth_routes = Blueprint('auth_routes', __name__)


auth_service = None

def init_routes(auth_svc):
    """Inicializa los servicios necesarios para las rutas."""
    global auth_service
    auth_service = auth_svc

@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Inicia sesión de un profesor.
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos JSON'
            }), 400
            
        if 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'error': 'Se requieren email y password'
            }), 400
        
        result = auth_service.login(data['email'], data['password'])
        
        if not result.get('success', False):
            return jsonify(result), 401
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_routes.route('/register', methods=['POST'])
def register():
    """
    Registra un nuevo profesor.
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos JSON'
            }), 400
            
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Se requiere el campo {field}'
                }), 400
        
        result = auth_service.register(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            school=data.get('school'),
            grade=data.get('grade')
        )
        
        if not result.get('success', False):
            return jsonify(result), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_routes.route('/profile', methods=['GET'])
def get_profile():
    """
    Obtiene el perfil del profesor autenticado.
    """
    try:
        # Obtener el token de autorización
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Se requiere token de autorización'
            }), 401
            
        token = auth_header.split(' ')[1]
        
        # Verificar el token
        token_result = auth_service.verify_token(token)
        
        if not token_result.get('valid', False):
            return jsonify({
                'success': False,
                'error': token_result.get('error', 'Token inválido')
            }), 401
        
        # Obtener información del profesor
        teacher_id = token_result.get('teacher_id')
        teacher = auth_service.get_teacher_by_id(teacher_id)
        
        if not teacher:
            return jsonify({
                'success': False,
                'error': 'Profesor no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'teacher': teacher
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_routes.route('/profile', methods=['PUT'])
def update_profile():
    """
    Actualiza el perfil del profesor autenticado.
    """
    try:
        # Obtener el token de autorización
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Se requiere token de autorización'
            }), 401
            
        token = auth_header.split(' ')[1]
        
        # Verificar el token
        token_result = auth_service.verify_token(token)
        
        if not token_result.get('valid', False):
            return jsonify({
                'success': False,
                'error': token_result.get('error', 'Token inválido')
            }), 401
        
        # Obtener datos de actualización
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos JSON'
            }), 400
        
        # Actualizar perfil
        teacher_id = token_result.get('teacher_id')
        result = auth_service.update_profile(teacher_id, data)
        
        if not result.get('success', False):
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500