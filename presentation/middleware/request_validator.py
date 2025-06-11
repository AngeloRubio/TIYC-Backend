from flask import request, jsonify
from functools import wraps
from pydantic import ValidationError

def validate_request(schema_class):
    """
    Decorador para validar los datos de entrada de las solicitudes usando Pydantic.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                # Obtener los datos de la solicitud
                if request.is_json:
                    data = request.json
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Se esperaba contenido JSON',
                        'error_type': 'validation_error'
                    }), 400
                
                #   Validar los datos usando el esquema de Pydantic
                #   Si la validación falla, se lanzará una excepción ValidationError
                validated_data = schema_class(**data)
                
                #   Si la validación es exitosa, se puede acceder a los datos validados
                #   a través de validated_data
                kwargs['validated_data'] = validated_data
                
                return f(*args, **kwargs)
            except ValidationError as e:
                # Convertir errores de Pydantic a un formato amigable
                errors = {}
                for error in e.errors():
                    location = '.'.join(str(loc) for loc in error['loc'])
                    errors[location] = error['msg']
                
                return jsonify({
                    'success': False,
                    'error': 'Errores de validación en la solicitud',
                    'error_type': 'validation_error',
                    'errors': errors
                }), 400
        return decorated
    return decorator