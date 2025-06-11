from typing import List, Optional
from uuid import UUID

from domain.entities.image import Image
from domain.interfaces.repositories.image_repository import ImageRepository
from infrastructure.database.connection import DatabaseConnection

class MySQLImageRepository(ImageRepository):
    """Implementación MySQL del repositorio de imágenes."""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create(self, image: Image) -> UUID:
        """Crea una nueva imagen en la base de datos."""
        query = """
        INSERT INTO images (id, scenario_id, prompt, image_url, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            str(image.id),
            str(image.scenario_id),
            image.prompt,
            image.image_url,
            image.created_at
        )
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
        
        return image.id
    
    def get_by_id(self, image_id: UUID) -> Optional[Image]:
        """Obtiene una imagen por su ID."""
        query = "SELECT * FROM images WHERE id = %s"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(image_id),))
            result = cursor.fetchone()
            
        if not result:
            return None
            
        return Image(
            id=UUID(result["id"]),
            scenario_id=UUID(result["scenario_id"]),
            prompt=result["prompt"],
            image_url=result["image_url"],
            created_at=result["created_at"]
        )
    
    def get_by_scenario_id(self, scenario_id: UUID) -> Optional[Image]:
        """Obtiene una imagen asociada a un escenario específico."""
        query = "SELECT * FROM images WHERE scenario_id = %s"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(scenario_id),))
            result = cursor.fetchone()
            
        if not result:
            return None
            
        return Image(
            id=UUID(result["id"]),
            scenario_id=UUID(result["scenario_id"]),
            prompt=result["prompt"],
            image_url=result["image_url"],
            created_at=result["created_at"]
        )
    
    def get_by_story_id(self, story_id: UUID) -> List[Image]:
        """Obtiene todas las imágenes asociadas a un cuento."""
        query = """
        SELECT i.* 
        FROM images i
        JOIN scenarios s ON i.scenario_id = s.id
        WHERE s.story_id = %s
        ORDER BY s.sequence_number
        """
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(story_id),))
            results = cursor.fetchall()
            
        images = []
        for result in results:
            images.append(Image(
                id=UUID(result["id"]),
                scenario_id=UUID(result["scenario_id"]),
                prompt=result["prompt"],
                image_url=result["image_url"],
                created_at=result["created_at"]
            ))
            
        return images
    
    def update(self, image: Image) -> bool:
        """Actualiza una imagen existente."""
        query = """
        UPDATE images
        SET prompt = %s, image_url = %s
        WHERE id = %s
        """
        values = (
            image.prompt,
            image.image_url,
            str(image.id)
        )
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
            return cursor.rowcount > 0
    
    def delete(self, image_id: UUID) -> bool:
        """Elimina una imagen por su ID."""
        query = "DELETE FROM images WHERE id = %s"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(image_id),))
            return cursor.rowcount > 0
    
    def delete_by_scenario_id(self, scenario_id: UUID) -> bool:
        """Elimina todas las imágenes asociadas a un escenario."""
        query = "DELETE FROM images WHERE scenario_id = %s"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(scenario_id),))
            return cursor.rowcount > 0