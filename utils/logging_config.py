import logging
import os
from logging.handlers import RotatingFileHandler

def configure_logging(app, log_level=logging.INFO):
    """
    Configura el sistema de logging para la aplicación Flask.
    """
    # Asegurar que el directorio de logs exista
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Crear el manejador de archivo con rotación
    log_file = os.path.join(logs_dir, 'app.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=10)
    
    # Definir formato para los logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # Configurar el logger de la aplicación Flask
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)
    
    # Configurar el logger raíz también
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(log_level)
    
    # Eliminar handlers por defecto
    app.logger.handlers = [file_handler]
    
    # Log de inicio
    app.logger.info('Logging configurado y aplicación iniciada')
    
    return app