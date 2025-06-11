from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class Scenario:
    """Entidad que representa un escenario o momento clave en un cuento."""
    
    def __init__(
        self,
        story_id: UUID,
        description: str,
        sequence_number: int,
        prompt_for_image: str,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.story_id = story_id
        self.description = description
        self.sequence_number = sequence_number
        self.prompt_for_image = prompt_for_image
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convierte la entidad a un diccionario."""
        return {
            "id": str(self.id),
            "story_id": str(self.story_id),
            "description": self.description,
            "sequence_number": self.sequence_number,
            "prompt_for_image": self.prompt_for_image,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Scenario':
        """Crea una instancia de Scenario a partir de un diccionario."""
        return cls(
            id=UUID(data["id"]) if data.get("id") else None,
            story_id=UUID(data["story_id"]),
            description=data["description"],
            sequence_number=data["sequence_number"],
            prompt_for_image=data["prompt_for_image"],
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        )