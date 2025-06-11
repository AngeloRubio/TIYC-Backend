from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

class Story:
    """Entidad que representa un cuento completo."""
    
    def __init__(
        self,
        title: str,
        content: str,
        context: str,
        category: str,
        pedagogical_approach: str = "traditional",  #tenemos la pedagogia tradicional como predefinida
        teacher_id: Optional[UUID] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.title = title
        self.content = content
        self.context = context
        self.category = category
        self.pedagogical_approach = pedagogical_approach
        self.teacher_id = teacher_id
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convierte la entidad a un diccionario."""
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "context": self.context,
            "category": self.category,
            "pedagogical_approach": self.pedagogical_approach,
            "teacher_id": str(self.teacher_id) if self.teacher_id else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Story':
        """Crea una instancia de Story a partir de un diccionario."""
        return cls(
            id=UUID(data["id"]) if data.get("id") else None,
            title=data["title"],
            content=data["content"],
            context=data["context"],
            category=data["category"],
            pedagogical_approach=data.get("pedagogical_approach", "traditional"),
            teacher_id=UUID(data["teacher_id"]) if data.get("teacher_id") else None,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        )