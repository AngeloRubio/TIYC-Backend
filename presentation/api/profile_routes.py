
from flask import Blueprint, request, jsonify
from functools import wraps

from application.services.teacher_profile_service import TeacherProfileService
from application.dtos.profile_dtos import UpdateProfileRequest, ChangePasswordRequest
from presentation.middleware.auth_middleware import auth_required
from presentation.middleware.error_handler import error_handler
from presentation.middleware.request_validator import validate_request

profile_routes = Blueprint('profile_routes', __name__)

profile_service = None

def init_routes(profile_svc):
    global profile_service
    profile_service = profile_svc


@profile_routes.route('/profile', methods=['GET'])
@auth_required
@error_handler
def get_profile(teacher_id: str):
    try:
        result = profile_service.get_profile(teacher_id)
        
        if not result.get("success", False):
            return jsonify({
                'success': False,
                'error': result.get("error", "Error al obtener perfil")
            }), 404 if "no encontrado" in result.get("error", "").lower() else 500
        
        return jsonify({
            'success': True,
            'profile': result["profile"]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@profile_routes.route('/profile', methods=['PUT'])
@auth_required
@error_handler
@validate_request(UpdateProfileRequest)
def update_profile(teacher_id: str, validated_data: UpdateProfileRequest):
    try:
        update_data = validated_data.dict(exclude_unset=True)
        
        if not update_data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        
        result = profile_service.update_profile(teacher_id, update_data)
        
        if not result.get("success", False):
            status_code = 400
            if "no encontrado" in result.get("error", "").lower():
                status_code = 404
            elif "Error interno" in result.get("error", ""):
                status_code = 500
                
            return jsonify({
                'success': False,
                'error': result.get("error", "Error al actualizar perfil"),
                'validation_errors': result.get("validation_errors", [])
            }), status_code
        
        return jsonify({
            'success': True,
            'profile': result["profile"],
            'message': result.get("message", "Perfil actualizado exitosamente")
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@profile_routes.route('/profile/password', methods=['PUT'])
@auth_required
@error_handler
@validate_request(ChangePasswordRequest)
def change_password(teacher_id: str, validated_data: ChangePasswordRequest):
    try:
        password_data = validated_data.dict()
        
        result = profile_service.change_password(teacher_id, password_data)
        
        if not result.get("success", False):
            status_code = 400
            if "no encontrado" in result.get("error", "").lower():
                status_code = 404
            elif "Error interno" in result.get("error", ""):
                status_code = 500
                
            return jsonify({
                'success': False,
                'error': result.get("error", "Error al cambiar contraseña"),
                'validation_errors': result.get("validation_errors", [])
            }), status_code
        
        return jsonify({
            'success': True,
            'message': result.get("message", "Contraseña cambiada exitosamente")
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@profile_routes.route('/profile/activity', methods=['GET'])
@auth_required
@error_handler
def get_activity_summary(teacher_id: str):
    try:
        result = profile_service.get_activity_summary(teacher_id)
        
        if not result.get("success", False):
            return jsonify({
                'success': False,
                'error': result.get("error", "Error al obtener resumen de actividad")
            }), 404 if "no encontrado" in result.get("error", "").lower() else 500
        
        return jsonify({
            'success': True,
            'summary': result["summary"]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@profile_routes.route('/profile/validate', methods=['POST'])
@auth_required
@error_handler  
def validate_profile_data(teacher_id: str):
    try:
        data = request.json
        
        if not data or 'field' not in data or 'value' not in data:
            return jsonify({
                'success': False,
                'error': 'Se requieren los campos "field" y "value"'
            }), 400
        
        field = data['field']
        value = data['value']
        
        if field == 'username':
            request_data = UpdateProfileRequest(username=value)
        elif field == 'school':
            request_data = UpdateProfileRequest(school=value)
        elif field == 'grade':
            request_data = UpdateProfileRequest(grade=value)
        else:
            return jsonify({
                'success': False,
                'error': 'Campo no válido'
            }), 400
        
        return jsonify({
            'success': True,
            'valid': True,
            'message': f'{field} es válido'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'valid': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@profile_routes.route('/profile/stats', methods=['GET'])
@auth_required
@error_handler
def get_profile_stats(teacher_id: str):
    try:
        period = request.args.get('period', 'month')
        include_charts = request.args.get('include_charts', 'false').lower() == 'true'
        
        stats = {
            "stories_by_month": {"2024-11": 3, "2024-12": 5, "2025-01": 2},
            "stories_by_category": {"Aventura": 4, "Ciencia": 3, "Fantasía": 3},
            "stories_by_approach": {"traditional": 6, "montessori": 3, "waldorf": 1},
            "average_story_length": 450.5,
            "most_active_day": "Miércoles"
        }
        
        if include_charts:
            stats["chart_data"] = {
                "monthly_activity": [
                    {"month": "Nov", "stories": 3},
                    {"month": "Dic", "stories": 5}, 
                    {"month": "Ene", "stories": 2}
                ],
                "category_distribution": [
                    {"category": "Aventura", "count": 4, "percentage": 40},
                    {"category": "Ciencia", "count": 3, "percentage": 30},
                    {"category": "Fantasía", "count": 3, "percentage": 30}
                ]
            }
        
        return jsonify({
            'success': True,
            'stats': stats,
            'period': period
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500