from typing import Optional
from pydantic import BaseModel, Field, field_validator



class GenerateStoryRequest(BaseModel):
    """DTO para solicitar la generación de un cuento."""

    context: str = Field(
        ..., min_length=10, description="Contexto o descripción para generar el cuento"
    )
    category: str = Field(
        ..., min_length=2, description="Categoría o género del cuento"
    )
    pedagogical_approach: str = Field(
        "traditional",
        description="Enfoque pedagógico: montessori, waldorf, traditional",
    )
    teacher_id: Optional[str] = Field(
        None, description="ID del profesor que solicita la generación"
    )
    target_age: Optional[str] = Field(
        None, description="Edad objetivo del cuento"
    )  # Lo tengo por defecto no se las edades de los cursos
    max_length: Optional[int] = Field(
        None, ge=100, le=5000, description="Longitud máxima del cuento en palabras"
    )
    num_illustrations: Optional[int] = Field(
        6, ge=1, le=20, description="Número de ilustraciones a generar"
    )


class GenerateImageRequest(BaseModel):
    """DTO para solicitar la generación de una imagen."""

    prompt: str = Field(..., min_length=10, description="Prompt para generar la imagen")
    pedagogical_approach: str = Field(
        "traditional",
        description="Enfoque pedagógico: montessori, waldorf, traditional",
    )
    style: Optional[str] = Field(
        "children_illustration", description="Estilo artístico de la imagen"
    )
    width: Optional[int] = Field(
        512, ge=256, le=1024, description="Ancho de la imagen en píxeles"
    )
    height: Optional[int] = Field(
        512, ge=256, le=1024, description="Alto de la imagen en píxeles"
    )


class UpdateProfileRequest(BaseModel):
    """DTO para actualización de perfil de profesor."""

    username: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Nombre de usuario"
    )
    school: Optional[str] = Field(
        None, min_length=3, max_length=100, description="Nombre de la escuela"
    )
    grade: Optional[str] = Field(None, description="Grado que enseña")

    @field_validator("username")
    def validate_username(cls, v):
        if v is not None:
            v = v.strip()
            if not v.replace(" ", "").replace("_", "").isalnum():
                raise ValueError(
                    "Username solo puede contener letras, números, espacios y guiones bajos"
                )
        return v

    @field_validator("grade")
    def validate_grade(cls, v):
        if v is not None:
            valid_grades = [
                "Primero de Básica",
                "Segundo de Básica",
                "Tercero de Básica",
                "Cuarto de Básica",
                "Quinto de Básica",
                "Sexto de Básica",
                "Séptimo de Básica",
            ]
            if v not in valid_grades:
                raise ValueError("Grado escolar no válido")
        return v


class ChangePasswordRequest(BaseModel):
    """DTO para cambio de contraseña."""

    current_password: str = Field(..., min_length=1, description="Contraseña actual")
    new_password: str = Field(..., min_length=8, description="Nueva contraseña")
    confirm_password: str = Field(
        ..., min_length=8, description="Confirmación de nueva contraseña"
    )

    @field_validator("confirm_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Las contraseñas no coinciden")
        return v
