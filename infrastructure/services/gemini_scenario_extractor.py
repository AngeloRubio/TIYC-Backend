from typing import List, Dict, Any
import os
import google.generativeai as genai

from domain.interfaces.services.scenario_extractor import ScenarioExtractorService

class GeminiScenarioExtractor(ScenarioExtractorService):
    """Implementación del extractor de escenarios usando Google Gemini."""
    
    def __init__(self, api_key: str = None):
        # Usar la clave de API proporcionada en el .env
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Se requiere la clave de API de Gemini") # en caso de que no se haya proporcionado (esto paso cambiando por momento por que no tenemos un usario clave para la implementacion)
        
        # Configurar la API de Gemini
        genai.configure(api_key=api_key)
        
        # Modelo a utilizar - Gemini 2.0 Flash de Google
        self.model_name = 'gemini-2.0-flash'
    
    def extract_scenarios(
        self, 
        title: str, 
        content: str, 
        num_scenarios: int = 6,
        pedagogical_approach: str = "traditional" # tenemos la pedagogia tradicional como predefinida
    ) -> List[Dict[str, Any]]:
        """
        Extrae los escenarios clave de un cuento para su ilustración.
        
        Args:
            title: Título del cuento
            content: Contenido completo del cuento
            num_scenarios: Número de escenarios a extraer
            pedagogical_approach: Enfoque pedagógico ("montessori", "waldorf", "traditional")
            
        Returns:
            Lista de escenarios con descripción y prompt para imagen
        """
        # Construir un prompt detallado para el modelo
        prompt = self._build_prompt(title, content, num_scenarios, pedagogical_approach)
        
        try:
            # Generar el análisis con Gemini
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            # Procesar la respuesta
            scenarios_text = response.text
            
            # Analizar la respuesta y convertirla en una lista de escenarios
            scenarios = self._parse_scenarios(scenarios_text)
            
            return scenarios
            
        except Exception as e:
            print(f"Error al extraer escenarios: {e}")
            # Retornar una lista vacía en caso de error
            return []
    
    def _build_prompt(self, title: str, content: str, num_scenarios: int, pedagogical_approach: str = "traditional") -> str:
        """
        Construye el prompt para el modelo de Gemini.
        """
        # Base del prompt esta en ingles por que el modelo no soporta español el de generacion de imagenes
        prompt = f"""
        TASK: You are an expert children's book illustrator tasked with creating a visual narrative from a story.

        PROCESS:
        1. First, carefully analyze the story to create a detailed "character bible":
           - Identify ALL main and secondary characters
           - For EACH character, extract EXACT details from the text:
             * Physical appearance (age, height, body type)
             * Hair (color, style, length, texture)
             * Facial features (eye color, distinctive features)
             * Clothing (ALL garments with SPECIFIC colors)
             * Accessories (backpacks, hats, glasses, jewelry)
             * Props/objects they use (tools, toys, items they carry)

        2. Next, identify {num_scenarios} key narrative moments that:
           - Follow chronological order
           - Show important plot developments
           - Include character actions and interactions
           - Capture emotional moments
           - Showcase important story objects/elements

        3. For EACH scene, create:
           - A brief scene description in Spanish
           - A highly detailed image prompt in English

        STORY TITLE: {title}
        
        STORY CONTENT:
        {content}

        CRITICAL REQUIREMENTS:
        - EVERY prompt must maintain 100% visual consistency with the character bible
        - EVERY detail from the story must be captured precisely (colors, objects, environment)
        - Characters should be doing specific actions from the story (not just standing/posing)
        - Include objects mentioned in the story that characters interact with
        - Scenes should have appropriate backgrounds that match the story setting
        - EVERY prompt must be in ENGLISH and highly detailed (200+ words)
        """
        
        # Instrucciones específicas según el enfoque pedagógico
        if pedagogical_approach.lower() == "montessori":
            prompt += """
            
            PEDAGOGICAL APPROACH: Montessori
            
            For this approach:
            - Show scientifically accurate depictions of real-world elements
            - Include precise details of natural materials and environments
            - Focus on characters actively engaged in problem-solving
            - Show realistic cause-and-effect relationships
            - Include real tools being used properly
            - Show children doing activities independently
            - Use natural color palettes (avoid fantasy colors)
            - Emphasize order, concentration, and purposeful work
            - Show realistic scale relationships between objects
            """
        elif pedagogical_approach.lower() == "waldorf":
            prompt += """
            
            PEDAGOGICAL APPROACH: Waldorf
            
            For this approach:
            - Create dreamlike, imaginative atmospheres with soft edges
            - Use watercolor-style aesthetic with gentle color transitions
            - Incorporate natural rhythms, seasons, and cycles
            - Show handcrafted objects and natural materials
            - Emphasize sensory-rich environments (textures, colors, light)
            - Include archetypal imagery and symbolic elements
            - Create a sense of wonder and reverence for nature
            - Avoid modern technology or artificial environments
            - Use flowing, organic forms rather than rigid structures
            """
        else:  # traditional
            prompt += """
            
            PEDAGOGICAL APPROACH: Traditional
            
            For this approach:
            - Use bright, vibrant colors that appeal to children
            - Create clearly defined characters with expressive faces
            - Include detailed backgrounds that enhance the storytelling
            - Emphasize key narrative moments with dramatic composition
            - Show clear emotional expressions on characters' faces
            - Include visual elements that reinforce the moral/lesson
            - Create a balance between realism and stylized illustration
            - Use visual hierarchy to focus attention on important elements
            - Create visually engaging scenes that invite exploration
            """
        
        # Formato esperado para la respuesta
        prompt += f"""
        
        Please present your analysis in the following JSON format:
        
        [
          {{
            "sequence_number": 1,
            "description": "Breve descripción en español de la primera escena clave",
            "prompt_for_image": "Ultra-detailed image prompt in English for scene 1, including ALL character details (clothing colors, specific objects they're holding, exact actions they're performing, detailed environment/setting, etc.)"
          }},
          ... until completing exactly {num_scenarios} scenes in chronological order
        ]
        
        FINAL CRITICAL INSTRUCTIONS:
        1. Characters MUST maintain EXACT same appearance across ALL scenes (same hair color/style, same clothing colors, same accessories)
        2. Include specific objects mentioned in the story (e.g., if a character has a compass, book, or special item)
        3. Make sure characters are performing specific ACTIONS mentioned in the story, not just standing still
        4. EVERY prompt must be in ENGLISH with extreme attention to detail
        5. Characters should have expressive faces showing appropriate emotions for each scene
        """
        return prompt
    
    def _parse_scenarios(self, scenarios_text: str) -> List[Dict[str, Any]]:
        """
        Analiza el texto de respuesta y lo convierte en una lista de escenarios.
        Si el formato no es el esperado, intenta extraer la información de manera alternativa.
        """
        import json
        import re
        
        # Eliminar cualquier texto antes o después del JSON
        json_match = re.search(r'\[\s*{.*}\s*\]', scenarios_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
        else:
            json_text = scenarios_text
        
        try:
            # Intentar parsear el JSON directamente
            scenarios = json.loads(json_text)
            return scenarios
        except json.JSONDecodeError:
            # Si falla, intentar extraer la información manualmente
            scenarios = []
            
            # Buscar patrones en el texto para extraer información
            pattern = r'"sequence_number":\s*(\d+).*?"description":\s*"([^"]*)".*?"prompt_for_image":\s*"([^"]*)"'
            matches = re.findall(pattern, scenarios_text, re.DOTALL)
            
            for match in matches:
                seq_num, description, prompt = match
                scenarios.append({
                    "sequence_number": int(seq_num),
                    "description": description.strip(),
                    "prompt_for_image": prompt.strip()
                })
            
            # Si aún no se puede extraer, crear escenarios genéricos
            if not scenarios:
                # Dividir el contenido en segmentos aproximadamente iguales
                content_lines = scenarios_text.strip().split('\n')
                segments = len(content_lines) // 6 + 1
                
                for i in range(1, 7):
                    start = (i-1) * segments
                    end = i * segments if i < 6 else None
                    segment = ' '.join(content_lines[start:end]).strip()
                    
                    scenarios.append({
                        "sequence_number": i,
                        "description": f"Escena {i} del cuento",
                        "prompt_for_image": f"Children's illustration of scene {i} from the story. {segment[:100]}"
                    })
            
            return scenarios