from functools import wraps
import traceback
from flask import request, jsonify

from application.services.auth_service import AuthenticationService

def auth_required(f):
    """
    Decorador para proteger rutas que requieren autenticación.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # Obtener el token de autorización
            print("DEBUG: Verificando autenticación")
            auth_header = request.headers.get('Authorization')

            print(f"DEBUG: Header de autorización: {auth_header}")
            if not auth_header or not auth_header.startswith('Bearer '):
                print("DEBUG: Token de autorización no proporcionado o inválido")
                return jsonify({
                    'success': False,
                    'error': 'Se requiere token de autorización'
                }), 401
                
            token = auth_header.split(' ')[1]
            
            # Verificar el token (obteniendo el servicio de autenticación globalmente)
            from app import auth_service
            token_result = auth_service.verify_token(token)
            
            if not token_result.get('valid', False):
                return jsonify({
                    'success': False,
                    'error': token_result.get('error', 'Token inválido')
                }), 401
            
            # Agregar el ID del profesor a los argumentos de la función
            kwargs['teacher_id'] = token_result.get('teacher_id')
            
            return f(*args, **kwargs)
        except Exception as e:
            print(f"DEBUG: Error en la autenticación: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': f'Error de autenticación: {str(e)}'
            }), 500
    return decorated