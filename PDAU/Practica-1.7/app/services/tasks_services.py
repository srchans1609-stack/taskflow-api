from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import models
from app import schemas


# 1. Obtener tareas con filtros y paginación
def get_all_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 10,
    project_id: Optional[int] = None,
    completed: Optional[bool] = None
) -> List[models.Task]:
    
    # Construye una consulta SQL dinámica sobre la tabla 'tasks':
    # Si el router le pasa 'project_id', añade WHERE project_id
    # Si el router le pasa 'completed', añade AND completed 
    # Finalmente aplica OFFSET (skip) y LIMIT (limit)
    
    query = db.query(models.Task)
    
    # Filtro por proyecto 
    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)
        
    # Filtro por estado completado 
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
        
    return query.offset(skip).limit(limit).all()



# Obtener una tarea por su ID

def get_task_by_id(db: Session, task_id: int) -> Optional[models.Task]:
    #Busca y devuelve la tarea con el ID indicado o None si no existe.
    return db.query(models.Task).filter(models.Task.id == task_id).first()



# Crear una nueva tarea
def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    #Inserta la tarea en la base de datos a partir del esquema Pydantic.
    new_task = models.Task(**task_in.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task



#  Estadísticas de tareas 
def get_tasks_summary(db: Session) -> dict:
    #Devuelve contadores útiles en lugar de recorrer todas las filas en memoria.
    total = db.query(models.Task).count()
    completed = db.query(models.Task).filter(models.Task.completed == True).count()
    pending = total - completed
    
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending
    }



# Editar una tarea existente

def update_task(db: Session, task: models.Task, task_in: schemas.TaskUpdate) -> models.Task:
    #Actualiza solo los campos enviados en el body
    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
        
    db.commit()
    db.refresh(task)
    return task



#  Eliminar una tarea

def delete_task(db: Session, task: models.Task) -> None:

    db.delete(task)
    db.commit()