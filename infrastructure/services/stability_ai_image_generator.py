import os
import requests
import json
import time
from PIL import Image
from typing import Dict, Any, Optional, Tuple
import uuid
import dotenv
import logging

from domain.interfaces.services.image_generator import ImageGeneratorService
from domain.exceptions.domain_exceptions import ImageGenerationException, ExternalServiceException

# Configurar logger para este módulo
logger = logging.getLogger(__name__)

class StabilityAIImageGenerator(ImageGeneratorService):
    """Implementación del generador de imágenes usando la API de Stability AI."""
    
    def __init__(self, api_key: Optional[str] = None, image_storage_path: Optional[str] = None):
        # Cargar variables de entorno
        dotenv.load_dotenv()
        
        # Obtener y verificar la API key
        self.api_key = api_key or os.getenv("STABILITY_API_KEY")
        if not self.api_key:
            logger.error("No se encontró la clave API de Stability AI")
            raise ValueError("Se requiere clave API de Stability AI. Configúrela en STABILITY_API_KEY.")
        
        logger.info(f"API key de Stability configurada: {self.api_key[:5]}...")
        
        # Configurar el directorio de almacenamiento de imágenes
        self.image_storage_path = image_storage_path or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..", "static/images")
        )
        
        # Crear directorio si no existe
        if not os.path.exists(self.image_storage_path):
            logger.info(f"Creando directorio de imágenes: {self.image_storage_path}")
            os.makedirs(self.image_storage_path, exist_ok=True)
        
        # URL base de la API
        self.api_base_url = "https://api.stability.ai/v2beta/stable-image/generate/core"
        logger.info("StabilityAIImageGenerator inicializado correctamente")
    
    def generate_image(
        self, 
        prompt: str,
        pedagogical_approach: str = "traditional",
        style: str = "children_illustration",
        width: int = 512,
        height: int = 512
    ) -> Dict[str, Any]:
        """
        Genera una imagen basada en el prompt proporcionado usando la API de Stability AI.
        """
        logger.info(f"Iniciando generación de imagen - Enfoque: {pedagogical_approach}")
        
        try:
            # Aplicar estilo pedagógico
            enhanced_prompt, negative_prompt, style_preset = self._apply_pedagogical_style(
                prompt, pedagogical_approach
            )
            
            # Determinar relación de aspecto
            aspect_ratio = self._get_aspect_ratio(width, height)
            
            # Configurar parámetros para la API
            params = {
                "prompt": enhanced_prompt,
                "negative_prompt": negative_prompt,
                "aspect_ratio": aspect_ratio,
                "seed": 0,
                "style_preset": style_preset,
                "output_format": "png"
            }
            
            # Realizar solicitud a la API
            response = self._send_generation_request(params)
            
            # Verificar filtro de contenido
            finish_reason = response.headers.get("finish-reason")
            if finish_reason == 'CONTENT_FILTERED':
                logger.warning("La generación no pasó el filtro de contenido de Stability AI")
                return {
                    "success": False,
                    "error": "La generación no pasó el filtro de contenido de Stability AI"
                }
            
            # Obtener semilla y guardar imagen
            seed = response.headers.get("seed", "unknown")
            filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join(self.image_storage_path, filename)
            
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            relative_path = f"/static/images/{filename}"
            
            logger.info(f"Imagen generada exitosamente - Seed: {seed}")
            
            return {
                "success": True,
                "image_url": relative_path,
                "prompt": enhanced_prompt,
                "pedagogical_approach": pedagogical_approach,
                "seed": seed
            }
            
        except ExternalServiceException as e:
            logger.error(f"Error de servicio externo: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error general al generar imagen: {str(e)}")
            raise ImageGenerationException(f"Error al generar imagen: {str(e)}")
    
    def _apply_pedagogical_style(
        self, 
        prompt: str, 
        pedagogical_approach: str
    ) -> Tuple[str, str, str]:
        """
        Aplica el estilo pedagógico al prompt y retorna prompt enriquecido, 
        negative_prompt y style_preset.
        """
        pedagogical_styles = {
            "montessori": {
                "prompt_suffix": "escena realista con materiales naturales, entorno ordenado, colores naturales y precisos, niños realizando actividades prácticas de forma independiente, ambiente con propósito, detalles precisos y científicamente correctos",
                "negative_prompt": "personajes de fantasía, colores irreales, escenas caóticas, elementos mágicos, personificación de animales, proporciones irreales, caricaturas",
                "style_preset": "photographic"
            },
            "waldorf": {
                "prompt_suffix": "ilustración estilo acuarela suave, colores pastel y cálidos, elementos orgánicos y naturales, sensación etérea y onírica, entorno armonioso inspirado en la naturaleza, elementos folclóricos tradicionales",
                "negative_prompt": "aspecto digital, líneas perfectas, colores artificiales o neón, tecnología moderna, entornos industriales, estilo minimalista",
                "style_preset": "fantasy-art"
            },
            "traditional": {
                "prompt_suffix": "ilustración infantil colorida y vívida, personajes expresivos y bien definidos, escena narrativa clara, colores brillantes, fondos detallados, estilo de libro ilustrado clásico",
                "negative_prompt": "estilo abstracto, escenas confusas, colores apagados o monótonos, elementos perturbadores",
                "style_preset": "digital-art"
            }
        }
        
        # Obtener configuración del estilo
        style_config = pedagogical_styles.get(
            pedagogical_approach.lower(), 
            pedagogical_styles["traditional"]
        )
        
        # Enriquecer el prompt
        enhanced_prompt = f"{prompt}, {style_config['prompt_suffix']}"
        
        return enhanced_prompt, style_config["negative_prompt"], style_config["style_preset"]
    
    def _send_generation_request(self, params):
        """Envía solicitud de generación a la API de Stability AI."""
        headers = {
            "Accept": "image/*",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            start_time = time.time()
            
            files = {}
            for key, value in params.items():
                files[key] = (None, str(value))

            response = requests.post(
                self.api_base_url,
                headers=headers,
                files=files
            )
            
            elapsed_time = time.time() - start_time
            logger.info(f"Respuesta de Stability AI recibida en {elapsed_time:.2f}s - Status: {response.status_code}")
            
            if not response.ok:
                error_message = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"Error en respuesta de Stability AI: {error_message}")
                raise ExternalServiceException("Stability AI", error_message)
            
            return response
            
        except requests.RequestException as e:
            logger.error(f"Error en solicitud HTTP a Stability AI: {str(e)}")
            raise ExternalServiceException("Stability AI", str(e))
    
    def _get_aspect_ratio(self, width: int, height: int) -> str:
        """
        Determina la relación de aspecto más cercana para Stability AI.
        """
        ratio = width / height
        
        # Mapear a las relaciones soportadas por Stability AI
        if ratio > 2.0:
            return "21:9"
        elif ratio > 1.6:  
            return "16:9"
        elif ratio > 1.4:  
            return "3:2"
        elif ratio > 1.1:  
            return "5:4"
        elif ratio > 0.9:
            return "1:1"
        elif ratio > 0.7:  
            return "4:5"
        elif ratio > 0.5:  
            return "2:3"
        elif ratio > 0.4:  
            return "9:16"
        else:
            return "9:21"