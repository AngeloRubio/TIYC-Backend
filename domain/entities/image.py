from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class Image:
    """Entidad que representa una imagen generada para un escenario."""
    
    def __init__(
        self,
        scenario_id: UUID,
        prompt: str,
        image_url: str,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.scenario_id = scenario_id
        self.prompt = prompt
        self.image_url = image_url
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convierte la entidad a un diccionario para estructurarlo en el json."""
        return {
            "id": str(self.id),
            "scenario_id": str(self.scenario_id),
            "prompt": self.prompt,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Image':
        """Crea una instancia de Image a partir de un diccionario."""
        return cls(
            id=UUID(data["id"]) if data.get("id") else None,
            scenario_id=UUID(data["scenario_id"]),
            prompt=data["prompt"],
            image_url=data["image_url"],
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        )