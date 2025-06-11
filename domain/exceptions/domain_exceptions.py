
class DomainException(Exception):
    """Excepción base para todas las excepciones de dominio."""
    pass


class EntityNotFoundException(DomainException):
    """Excepción lanzada cuando no se encuentra una entidad."""
    def __init__(self, entity_type, entity_id=None):
        self.entity_type = entity_type
        self.entity_id = entity_id
        message = f"{entity_type} no encontrado"
        if entity_id:
            message += f" con ID: {entity_id}"
        super().__init__(message)


class ValidationException(DomainException):
    """Excepción lanzada cuando hay errores de validación."""
    def __init__(self, message, errors=None):
        self.errors = errors or {}
        super().__init__(message)


class StoryGenerationException(DomainException):
    """Excepción lanzada cuando hay errores en la generación de cuentos."""
    pass


class ScenarioExtractionException(DomainException):
    """Excepción lanzada cuando hay errores en la extracción de escenarios."""
    pass


class ImageGenerationException(DomainException):
    """Excepción lanzada cuando hay errores en la generación de imágenes."""
    pass


class RepositoryException(DomainException):
    """Excepción lanzada cuando hay errores en los repositorios."""
    pass


class ExternalServiceException(DomainException):
    """Excepción lanzada cuando hay errores en servicios externos."""
    def __init__(self, service_name, message, original_error=None):
        self.service_name = service_name
        self.original_error = original_error
        super().__init__(f"Error en servicio externo {service_name}: {message}")