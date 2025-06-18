from typing import Optional
from pydantic import BaseModel, Field, field_validator

class UpdateProfileRequest(BaseModel):
    """DTO para actualización de perfil de profesor."""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Nombre de usuario")
    school: Optional[str] = Field(None, max_length=100, description="Nombre de la escuela")
    grade: Optional[str] = Field(None, max_length=50, description="Grado que enseña")
    
    @field_validator('username')
    def validate_username(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('El nombre de usuario no puede estar vacío')
            if len(v.strip()) < 3:
                raise ValueError('El nombre de usuario debe tener al menos 3 caracteres')
        return v.strip() if v else v
    
    @field_validator('school')
    def validate_school(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre de la escuela no puede estar vacío')
        return v.strip() if v else v
    
    @field_validator('grade')
    def validate_grade(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El grado no puede estar vacío')
        return v.strip() if v else v


class ChangePasswordRequest(BaseModel):
    """DTO para cambio de contraseña."""
    current_password: str = Field(..., min_length=1, description="Contraseña actual")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña")
    confirm_password: str = Field(..., min_length=6, description="Confirmación de nueva contraseña")
    
    @field_validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 6:
            raise ValueError('La nueva contraseña debe tener al menos 6 caracteres')
        return v
    
    @field_validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Las contraseñas no coinciden')
        return v


class ProfileResponse(BaseModel):
    """DTO para respuesta de perfil."""
    id: str
    username: str
    email: str
    school: Optional[str] = None
    grade: Optional[str] = None
    created_at: str


class ActivitySummaryResponse(BaseModel):
    """DTO para resumen de actividad del profesor."""
    total_stories: int
    stories_this_month: int
    favorite_category: Optional[str] = None
    favorite_approach: Optional[str] = None
    last_story_date: Optional[str] = None
    stories_by_month: dict
    stories_by_category: dict