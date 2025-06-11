from typing import Optional
from pydantic import BaseModel, Field

class GenerateStoryRequest(BaseModel):
    """DTO para solicitar la generación de un cuento."""
    context: str = Field(..., min_length=10, description="Contexto o descripción para generar el cuento")
    category: str = Field(..., min_length=2, description="Categoría o género del cuento")
    pedagogical_approach: str = Field("traditional", description="Enfoque pedagógico: montessori, waldorf, traditional")
    teacher_id: Optional[str] = Field(None, description="ID del profesor que solicita la generación")
    target_age: Optional[str] = Field(None, description="Edad objetivo del cuento") #Lo tengo por defecto no se las edades de los cursos
    max_length: Optional[int] = Field(None, ge=100, le=5000, description="Longitud máxima del cuento en palabras")
    num_illustrations: Optional[int] = Field(6, ge=1, le=20, description="Número de ilustraciones a generar") 

class GenerateImageRequest(BaseModel):
    """DTO para solicitar la generación de una imagen."""
    prompt: str = Field(..., min_length=10, description="Prompt para generar la imagen")
    pedagogical_approach: str = Field("traditional", description="Enfoque pedagógico: montessori, waldorf, traditional")
    style: Optional[str] = Field("children_illustration", description="Estilo artístico de la imagen")
    width: Optional[int] = Field(512, ge=256, le=1024, description="Ancho de la imagen en píxeles")
    height: Optional[int] = Field(512, ge=256, le=1024, description="Alto de la imagen en píxeles")