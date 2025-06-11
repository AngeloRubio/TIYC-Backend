from typing import List, Optional
from uuid import UUID

from domain.entities.scenario import Scenario
from domain.interfaces.repositories.scenario_repository import ScenarioRepository
from infrastructure.database.connection import DatabaseConnection

class MySQLScenarioRepository(ScenarioRepository):
    """Implementación MySQL del repositorio de escenarios."""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create(self, scenario: Scenario) -> UUID:
        """Crea un nuevo escenario en la base de datos."""
        query = """
        INSERT INTO scenarios (id, story_id, description, sequence_number, prompt_for_image, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            str(scenario.id),
            str(scenario.story_id),
            scenario.description,
            scenario.sequence_number,
            scenario.prompt_for_image,
            scenario.created_at
        )
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
        
        return scenario.id
    
    def get_by_id(self, scenario_id: UUID) -> Optional[Scenario]:
        """Obtiene un escenario por su ID."""
        query = "SELECT * FROM scenarios WHERE id = %s"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(scenario_id),))
            result = cursor.fetchone()
            
        if not result:
            return None
            
        return Scenario(
            id=UUID(result["id"]),
            story_id=UUID(result["story_id"]),
            description=result["description"],
            sequence_number=result["sequence_number"],
            prompt_for_image=result["prompt_for_image"],
            created_at=result["created_at"]
        )
    
    def get_by_story_id(self, story_id: UUID) -> List[Scenario]:
        """Obtiene todos los escenarios asociados a un cuento."""
        query = "SELECT * FROM scenarios WHERE story_id = %s ORDER BY sequence_number"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(story_id),))
            results = cursor.fetchall()
            
        scenarios = []
        for result in results:
            scenarios.append(Scenario(
                id=UUID(result["id"]),
                story_id=UUID(result["story_id"]),
                description=result["description"],
                sequence_number=result["sequence_number"],
                prompt_for_image=result["prompt_for_image"],
                created_at=result["created_at"]
            ))
            
        return scenarios
    
    def update(self, scenario: Scenario) -> bool:
        """Actualiza un escenario existente."""
        query = """
        UPDATE scenarios
        SET description = %s, sequence_number = %s, prompt_for_image = %s
        WHERE id = %s
        """
        values = (
            scenario.description,
            scenario.sequence_number,
            scenario.prompt_for_image,
            str(scenario.id)
        )
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
            return cursor.rowcount > 0
    
    def delete(self, scenario_id: UUID) -> bool:
        """Elimina un escenario por su ID."""
        query = "DELETE FROM scenarios WHERE id = %s"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(scenario_id),))
            return cursor.rowcount > 0
    
    def delete_by_story_id(self, story_id: UUID) -> bool:
        """Elimina todos los escenarios asociados a un cuento."""
        query = "DELETE FROM scenarios WHERE story_id = %s"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(story_id),))
            return cursor.rowcount > 0