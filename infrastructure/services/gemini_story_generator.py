import os
from typing import Dict, Any, Optional
import google.generativeai as genai

from domain.interfaces.services.story_generator import StoryGeneratorService

class GeminiStoryGenerator(StoryGeneratorService):
    """Implementación del generador de cuentos usando Google Gemini."""
    
    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Se requiere la clave de API de Gemini")
        
        # Configurar la API de Gemini
        genai.configure(api_key=api_key)
        
        # Modelo a utilizar
        self.model_name = 'gemini-2.0-flash'
    
    def generate_story(
        self, 
        context: str, 
        category: str,
        pedagogical_approach: str = "traditional",
        target_age: Optional[str] = None,
        max_length: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Genera un cuento basado en el contexto y la categoría proporcionados.
        """
        # Construir un prompt detallado para el modelo
        prompt = self._build_prompt(
            context, 
            category, 
            pedagogical_approach,
            target_age, 
            max_length
        )
        
        try:
            # Generar el contenido con Gemini
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            # Procesar la respuesta
            content = response.text
            
            # Extraer título y contenido
            lines = content.strip().split('\n')
            title = lines[0].strip()
            
            # Eliminar caracteres especiales del título como "#" si está formateado en Markdown
            title = title.lstrip('#').strip()
            
            # El resto es el contenido
            story_content = '\n'.join(lines[1:]).strip()
            
            return {
                "success": True,
                "title": title,
                "content": story_content
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_prompt(
        self, 
        context: str, 
        category: str,
        pedagogical_approach: str = "traditional",
        target_age: Optional[str] = None,
        max_length: Optional[int] = None
    ) -> str:
        """
        Construye el prompt para el modelo de Gemini.
        """
        # Base del prompt
        prompt = f"""
        Escribe un cuento infantil completo basado en la siguiente descripción:
        
        CONTEXTO: {context}
        CATEGORÍA: {category}
        """
        
        # Añadir instrucciones según el enfoque pedagógico
        if pedagogical_approach.lower() == "montessori":
            prompt += """
            
            Este cuento debe seguir los principios Montessori:
            - Centrarse en situaciones realistas y prácticas del mundo real
            - Presentar a los protagonistas resolviendo problemas por sí mismos
            - Usar lenguaje preciso y científicamente correcto
            - Mostrar consecuencias naturales en lugar de castigos artificiales
            - Incluir actividades que los niños puedan recrear por sí mismos
            - Limitar los elementos fantásticos y enfocarse en lo que el niño puede experimentar
            - Respetar la capacidad del niño para comprender el mundo
            """
        elif pedagogical_approach.lower() == "waldorf":
            prompt += """
            
            Este cuento debe seguir los principios Waldorf:
            - Incorporar elementos de fantasía, simbolismo y arquetipos
            - Conectar con los ritmos de la naturaleza y las estaciones
            - Incluir descripciones ricas y sensoriales (colores, texturas, sonidos)
            - Permitir que la moraleja surja orgánicamente sin ser didáctico
            - Presentar personajes arquetípicos en lugar de personajes planos
            - Fomentar la imaginación y el asombro
            - Incluir elementos artísticos o musicales cuando sea posible
            """
        else:  # traditional
            prompt += """
            
            Este cuento debe seguir un enfoque tradicional:
            - Tener una estructura clara con inicio, desarrollo y conclusión
            - Incluir personajes bien definidos con características identificables
            - Presentar una moraleja o lección clara al final
            - Combinar elementos de fantasía y realidad según sea necesario
            - Transmitir valores o enseñanzas específicas
            - Ser entretenido a la vez que educativo
            """
        
        # Añadir especificación de edad si se proporciona
        if target_age:
            prompt += f"\n\nEl cuento debe ser adecuado para niños de {target_age}."
        
        # Añadir restricción de longitud si se proporciona
        if max_length:
            prompt += f"\n\nEl cuento debe tener aproximadamente {max_length} palabras."
        
        # Añadir instrucciones adicionales generales
        prompt += """
        
        El cuento debe:
        - Tener un título creativo y atractivo
        - Incluir personajes memorables
        - Tener un inicio, desarrollo y conclusión claros
        - Transmitir un mensaje positivo o enseñanza
        - Ser adecuado para niños
        - Tener un lenguaje claro y sencillo
        - Ser original y creativo
        
        Por favor, comienza con el título en la primera línea y luego el contenido del cuento.
        """
        
        return prompt