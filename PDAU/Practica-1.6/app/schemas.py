from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Los schemas de Pydantic definen el contrato de datos de entrada/salida de la API.
# Se diferencian de los modelos de BD en que no gestionan la persistencia, 
# sino la validación, tipado y serialización de la interfaz HTTP.


#  SCHEMAS DE CATEGORY

class CategoryBase(BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="Nombre de la categoría (entre 1 y 100 caracteres)"
    )

class CategoryCreate(CategoryBase):
    """Schema de entrada para registrar una categoría."""
    pass

class CategoryUpdate(BaseModel):
    """Schema de entrada para editar una categoría (todos los campos opcionales)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)

#  SCHEMAS DE PROJECT
class ProjectBase(BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="Nombre del proyecto (entre 1 y 100 caracteres)"
    )
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        description="Descripción opcional del proyecto"
    )

class ProjectCreate(ProjectBase):
    """Schema de entrada para registrar un proyecto."""
    pass

class ProjectUpdate(BaseModel):
    """Schema de entrada para editar un proyecto (todos los campos opcionales)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ProjectRead(ProjectCreate):
    """Schema de salida con el detalle del proyecto y sus tareas asociadas."""
    id: int = Field(..., gt=0, description="Identificador único del proyecto")
    created_at: Optional[datetime] = Field(None, description="Fecha y hora de creación")
    
    # Devuelve automáticamente la lista de tareas del proyecto
    tasks: List[TaskRead] = []

    model_config = ConfigDict(from_attributes=True)


#  SCHEMAS DE TASK

class TaskBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="Título de la tarea (entre 1 y 100 caracteres)"
    )
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        description="Descripción opcional de la tarea"
    )
    project_id: int = Field(
        ..., 
        gt=0, 
        escription="Identificador del proyecto al que pertenece la tarea"
    )
    category_id: Optional[int] = Field(
        None,
        gt=0,
        description="Identificador de la categoría a la que pertenece la tarea (opcional)"
    )

class TaskCreate(TaskBase):
    """Schema de entrada para registrar una tarea."""
    pass

class TaskUpdate(BaseModel):
    """Schema de entrada para editar una tarea (todos los campos opcionales)."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = Field(None, description="Estado de la tarea")
    project_id: Optional[int] = Field(None, gt=0)
    category_id: Optional[int] = Field(None, gt=0)

class TaskRead(TaskBase):
    """Schema de salida con los datos de la tarea."""
    id: int = Field(..., gt=0, description="Identificador único de la tarea")
    completed: bool = Field(default=False, description="Estado de la tarea")
    created_at: Optional[datetime] = Field(None, description="Fecha y hora de creación")

    model_config = ConfigDict(from_attributes=True)