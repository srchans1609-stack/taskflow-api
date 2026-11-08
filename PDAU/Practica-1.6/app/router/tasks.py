from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app import schemas
from app.services import tasks_services

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# 1. GET /tasks -> Listar tareas con filtros y paginación
@router.get("/", response_model=List[schemas.TaskRead])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    project_id: Optional[int] = Query(None),
    completed: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    return tasks_services.get_all_tasks(db, skip=skip, limit=limit, project_id=project_id, completed=completed)

# Resumen de tareas (DEBE ir antes de /{task_id})
@router.get("/summary")
def get_tasks_summary(db: Session = Depends(get_db)):
    return tasks_services.get_tasks_summary(db)

# 2. GET /tasks/{task_id} -> Detalle de tarea
@router.get("/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = tasks_services.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return task

# 3. POST /tasks -> Crear tarea
@router.post("/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    return tasks_services.create_task(db, task_in)

# 4. PUT /tasks/{task_id} -> Editar tarea
@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = tasks_services.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return tasks_services.update_task(db, task, task_in)

# 5. DELETE /tasks/{task_id} -> Eliminar tarea
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = tasks_services.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    tasks_services.delete_task(db, task)
    return None