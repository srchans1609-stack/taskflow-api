from datetime import datetime
from typing import Optional, List 
from pydantic import BaseModel, Field, ConfigDict

# 1. SCHEMAS DE TASK (Deben ir primero para que Project y Category puedan usarlos)
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=500, description="Descripción opcional")
    project_id: int = Field(..., gt=0, description="Identificador del proyecto") # Corregido typo
    category_id: Optional[int] = Field(None, gt=0, description="Identificador de la categoría")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = Field(None, description="Estado de la tarea")
    project_id: Optional[int] = Field(None, gt=0)
    category_id: Optional[int] = Field(None, gt=0)

class TaskRead(TaskBase):
    id: int = Field(..., gt=0, description="Identificador único")
    completed: bool = Field(default=False, description="Estado de la tarea")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")

    model_config = ConfigDict(from_attributes=True)


# 2. SCHEMAS DE PROJECT
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ProjectRead(ProjectCreate):
    id: int = Field(..., gt=0)
    created_at: Optional[datetime] = Field(None)
    tasks: List[TaskRead] = []  # Ahora sí funciona porque TaskRead ya existe

    model_config = ConfigDict(from_attributes=True)


# 3. SCHEMAS DE CATEGORY
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class CategoryRead(CategoryBase):
    id: int = Field(..., gt=0)
    tasks: List[TaskRead] = [] 
    
    model_config = ConfigDict(from_attributes=True)