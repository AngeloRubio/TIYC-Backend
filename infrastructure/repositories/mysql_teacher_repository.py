from typing import List, Optional
from uuid import UUID
import bcrypt

from domain.entities.teacher import Teacher
from domain.interfaces.repositories.teacher_repository import TeacherRepository
from infrastructure.database.connection import DatabaseConnection

class MySQLTeacherRepository(TeacherRepository):
    """Implementación MySQL del repositorio de profesores."""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create(self, teacher: Teacher) -> UUID:
        """Crea un nuevo profesor en la base de datos."""
        query = """
        INSERT INTO teachers (id, username, email, password_hash, school, grade, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            str(teacher.id),
            teacher.username,
            teacher.email,
            teacher.password_hash,
            teacher.school,
            teacher.grade,
            teacher.created_at
        )
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
        
        return teacher.id
    
    def get_by_id(self, teacher_id: UUID) -> Optional[Teacher]:
        """Obtiene un profesor por su ID."""
        query = "SELECT * FROM teachers WHERE id = %s"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(teacher_id),))
            result = cursor.fetchone()
            
        if not result:
            return None
            
        return Teacher(
            id=UUID(result["id"]),
            username=result["username"],
            email=result["email"],
            password_hash=result["password_hash"],
            school=result["school"],
            grade=result["grade"],
            created_at=result["created_at"]
        )
    
    def get_by_email(self, email: str) -> Optional[Teacher]:
        """Obtiene un profesor por su email."""
        query = "SELECT * FROM teachers WHERE email = %s"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            
        if not result:
            return None
            
        return Teacher(
            id=UUID(result["id"]),
            username=result["username"],
            email=result["email"],
            password_hash=result["password_hash"],
            school=result["school"],
            grade=result["grade"],
            created_at=result["created_at"]
        )
    
    def update(self, teacher: Teacher) -> bool:
        """Actualiza un profesor existente."""
        query = """
        UPDATE teachers
        SET username = %s, email = %s, password_hash = %s, school = %s, grade = %s
        WHERE id = %s
        """
        values = (
            teacher.username,
            teacher.email,
            teacher.password_hash,
            teacher.school,
            teacher.grade,
            str(teacher.id)
        )
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
            return cursor.rowcount > 0
    
    def delete(self, teacher_id: UUID) -> bool:
        """Elimina un profesor por su ID."""
        query = "DELETE FROM teachers WHERE id = %s"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(teacher_id),))
            return cursor.rowcount > 0