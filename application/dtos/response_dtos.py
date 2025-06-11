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
