
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la base de datos
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "angelo"),
    "database": os.getenv("DB_NAME", "santa_fe"),
}

# Directorio para almacenar imágenes
IMAGE_STORAGE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "static/images")
)

# Asegurar que el directorio exista
os.makedirs(IMAGE_STORAGE_PATH, exist_ok=True)

# Configuración de API keys para servicios externos
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

# Configuración predeterminada para generación de cuentos
DEFAULT_NUM_ILLUSTRATIONS = 6
DEFAULT_IMAGE_STYLE = "children_illustration"
DEFAULT_IMAGE_WIDTH = 512
DEFAULT_IMAGE_HEIGHT = 512

# Relaciones de aspecto disponibles para Stability AI
STABILITY_ASPECT_RATIOS = ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]

# Formatos de salida disponibles para Stability AI
STABILITY_OUTPUT_FORMATS = ["webp", "jpeg", "png"]

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "angelo")