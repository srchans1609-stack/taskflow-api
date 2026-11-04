from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.db import models
from app import schemas

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# 1. GET /tasks (Filtros: project_id, completed | Paginación: skip, limit)
@router.get("/", response_model=List[schemas.TaskRead])
def get_tasks(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, ge=1, description="Límite de registros a devolver"),
    project_id: Optional[int] = Query(None, description="Filtrar por proyecto"),
    completed: Optional[bool] = Query(None, description="Filtrar por estado completado"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)
    
    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
        
    return query.offset(skip).limit(limit).all()


@router.get("/{id}", response_model=schemas.TaskRead)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.post("/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/{id}", response_model=schemas.TaskRead)
def update_task(id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Actualiza dinámicamente solo los campos enviados en el body
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
        
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return None