import uuid
import re
from typing import Dict, Any, Optional, List

def generate_uuid():
    """
    Genera un UUID único para identificadores de entidades.
    """
    return str(uuid.uuid4())

def sanitize_filename(filename):
    """
    Sanitiza un nombre de archivo para hacerlo seguro para el sistema de archivos.
    """
    # Reemplazar caracteres no seguros con guiones bajos
    sanitized = re.sub(r'[^\w\.-]', '_', filename)
    
    # Evitar nombres de archivo demasiado largos
    if len(sanitized) > 100:
        # Mantener la extensión si existe
        parts = sanitized.rsplit('.', 1)
        if len(parts) > 1:
            sanitized = parts[0][:96] + '.' + parts[1]
        else:
            sanitized = sanitized[:100]
    
    return sanitized

def paginate_results(items: List[Dict[str, Any]], page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """
    Pagina una lista de resultados.
    """
    # Validar parámetros
    page = max(1, page)
    page_size = max(1, min(100, page_size))
    
    # Calcular índices
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    # Obtener los elementos de la página actual
    paginated_items = items[start_idx:end_idx]
    
    # Calcular información de paginación
    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size
    
    return {
        'items': paginated_items,
        'page': page,
        'page_size': page_size,
        'total_items': total_items,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }