from typing import List, Optional
from uuid import UUID
import datetime

from domain.entities.story import Story
from domain.interfaces.repositories.story_repository import StoryRepository
from infrastructure.database.connection import DatabaseConnection

class MySQLStoryRepository(StoryRepository):
    """Implementación MySQL del repositorio de cuentos."""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create(self, story: Story) -> UUID:
        """Crea un nuevo cuento en la base de datos."""
        query = """
        INSERT INTO stories (id, title, content, context, category, pedagogical_approach, teacher_id, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            str(story.id), 
            story.title, 
            story.content, 
            story.context, 
            story.category,
            story.pedagogical_approach,  # ✅ Agregado el campo faltante
            str(story.teacher_id) if story.teacher_id else None,
            story.created_at
        )
        
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(query, values)
            print(f"✅ Cuento creado en BD con ID: {story.id}")
            return story.id
        except Exception as e:
            print(f"❌ Error al crear cuento en BD: {str(e)}")
            raise e
    
    def get_by_id(self, story_id: UUID) -> Optional[Story]:
        """Obtiene un cuento por su ID."""
        query = "SELECT * FROM stories WHERE id = %s"
        
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(query, (str(story_id),))
                result = cursor.fetchone()
                
            if not result:
                print(f"❌ Cuento no encontrado en BD: {story_id}")
                return None
                
            # Convertir teacher_id a UUID si no es None
            teacher_id = None
            if result["teacher_id"]:
                teacher_id = UUID(result["teacher_id"])
                
            story = Story(
                id=UUID(result["id"]),
                title=result["title"],
                content=result["content"],
                context=result["context"],
                category=result["category"],
                pedagogical_approach=result.get("pedagogical_approach", "traditional"),  # ✅ Con valor por defecto
                teacher_id=teacher_id,
                created_at=result["created_at"]
            )
            
            print(f"✅ Cuento encontrado en BD: {story.title}")
            return story
            
        except Exception as e:
            print(f"❌ Error al obtener cuento por ID: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_by_teacher_id(self, teacher_id: UUID, limit: int = 10) -> List[Story]:
        """Obtiene los cuentos creados por un profesor específico."""
        query = "SELECT * FROM stories WHERE teacher_id = %s ORDER BY created_at DESC LIMIT %s"
        
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(query, (str(teacher_id), limit))
                results = cursor.fetchall()
                
            stories = []
            for result in results:
                teacher_id_obj = None
                if result["teacher_id"]:
                    teacher_id_obj = UUID(result["teacher_id"])
                    
                stories.append(Story(
                    id=UUID(result["id"]),
                    title=result["title"],
                    content=result["content"],
                    context=result["context"],
                    category=result["category"],
                    pedagogical_approach=result.get("pedagogical_approach", "traditional"),  # ✅ Con valor por defecto
                    teacher_id=teacher_id_obj,
                    created_at=result["created_at"]
                ))
                
            print(f"✅ Se encontraron {len(stories)} cuentos del profesor en BD")
            return stories
            
        except Exception as e:
            print(f"❌ Error al obtener cuentos por profesor: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_recent(self, limit: int = 10) -> List[Story]:
        """Obtiene los cuentos más recientes."""
        query = "SELECT * FROM stories ORDER BY created_at DESC LIMIT %s"
        
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(query, (limit,))
                results = cursor.fetchall()
                
            stories = []
            for result in results:
                teacher_id_obj = None
                if result["teacher_id"]:
                    teacher_id_obj = UUID(result["teacher_id"])
                    
                stories.append(Story(
                    id=UUID(result["id"]),
                    title=result["title"],
                    content=result["content"],
                    context=result["context"],
                    category=result["category"],
                    pedagogical_approach=result.get("pedagogical_approach", "traditional"),  # ✅ Con valor por defecto
                    teacher_id=teacher_id_obj,
                    created_at=result["created_at"]
                ))
                
            print(f"✅ Se encontraron {len(stories)} cuentos recientes en BD")
            return stories
            
        except Exception as e:
            print(f"❌ Error al obtener cuentos recientes: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def update(self, story: Story) -> bool:
        """Actualiza un cuento existente."""
        query = """
        UPDATE stories
        SET title = %s, content = %s, context = %s, category = %s, pedagogical_approach = %s, teacher_id = %s
        WHERE id = %s
        """
        values = (
            story.title,
            story.content,
            story.context,
            story.category,
            story.pedagogical_approach,  # ✅ Incluido en UPDATE
            str(story.teacher_id) if story.teacher_id else None,
            str(story.id)
        )
        
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(query, values)
                success = cursor.rowcount > 0
                
            if success:
                print(f"✅ Cuento actualizado en BD: {story.id}")
            else:
                print(f"❌ No se actualizó ningún cuento: {story.id}")
            return success
            
        except Exception as e:
            print(f"❌ Error al actualizar cuento: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def delete(self, story_id: UUID) -> bool:
        """Elimina un cuento por su ID."""
        query = "DELETE FROM stories WHERE id = %s"
        
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(query, (str(story_id),))
                success = cursor.rowcount > 0
                
            if success:
                print(f"✅ Cuento eliminado de BD: {story_id}")
            else:
                print(f"❌ No se eliminó ningún cuento: {story_id}")
            return success
            
        except Exception as e:
            print(f"❌ Error al eliminar cuento: {str(e)}")
            import traceback
            traceback.print_exc()
            return False