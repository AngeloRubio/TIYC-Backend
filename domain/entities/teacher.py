from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

class Teacher:
    """Entidad que representa a un profesor/usuario del sistema."""
    
    def __init__(
        self,
        username: str,
        email: str,
        password_hash: str,
        school: Optional[str] = None,
        grade: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.school = school
        self.grade = grade
        self.created_at = created_at or datetime.now()
    
    def to_dict(self, exclude: List[str] = None) -> Dict[str, Any]:
        """Convierte la entidad a un diccionario."""
        exclude = exclude or []
        data = {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "school": self.school,
            "grade": self.grade,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if "password_hash" not in exclude:
            data["password_hash"] = self.password_hash
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Teacher':
        """Crea una instancia de Teacher a partir de un diccionario."""
        return cls(
            id=UUID(data["id"]) if data.get("id") else None,
            username=data["username"],
            email=data["email"],
            password_hash=data["password_hash"],
            school=data.get("school"),
            grade=data.get("grade"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        )
        
    def has_access_to_story(self, story_id: UUID) -> bool:
        """Verifica si el profesor tiene acceso a un cuento específico."""
        # Por ahora, simplemente verificamos que el profesor sea el propietario del cuento
        from application.services.story_service import StoryService
        story = StoryService.get_story_by_id(str(story_id))
        if not story:
            return False
        return story.get("teacher_id") == str(self.id)