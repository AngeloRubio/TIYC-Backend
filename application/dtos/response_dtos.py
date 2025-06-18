from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class StoryResponse(BaseModel):
    """DTO para la respuesta de un cuento."""
    id: str
    title: str
    content: str
    context: str
    category: str
    teacher_id: Optional[str] = None
    created_at: datetime

class ScenarioResponse(BaseModel):
    """DTO para la respuesta de un escenario."""
    id: str
    story_id: str
    description: str
    sequence_number: int
    prompt_for_image: str
    created_at: datetime
    image: Optional[Dict[str, Any]] = None

class ImageResponse(BaseModel):
    """DTO para la respuesta de una imagen."""
    id: str
    scenario_id: str
    prompt: str
    image_url: str
    created_at: datetime

class IllustratedStoryResponse(BaseModel):
    """DTO para la respuesta de un cuento completo (imagenes y escenarios)."""
    story: StoryResponse
    scenarios: List[ScenarioResponse]
# Agregar al final de application/dtos/response_dtos.py

class ProfileResponse(BaseModel):
    """DTO para respuesta de perfil completo."""
    
    id: str
    username: str
    email: str
    school: Optional[str] = None
    grade: Optional[str] = None
    created_at: str
    profile_completion: int = Field(default=0, ge=0, le=100, description="Porcentaje de completitud")
    story_count: int = Field(default=0, ge=0, description="Total de cuentos creados")
    last_activity: Optional[str] = None