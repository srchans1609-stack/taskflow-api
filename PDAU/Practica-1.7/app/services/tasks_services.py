from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import models
from app import schemas

def get_all_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 10,
    project_id: Optional[int] = None,
    completed: Optional[bool] = None
) -> List[models.Task]:
    query = db.query(models.Task)
    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    return query.offset(skip).limit(limit).all()

def get_task_by_id(db: Session, task_id: int) -> Optional[models.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    new_task = models.Task(**task_in.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks_summary(db: Session) -> dict:
    total = db.query(models.Task).count()
    completed = db.query(models.Task).filter(models.Task.completed == True).count()
    pending = total - completed
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending
    }

def update_task(db: Session, task: models.Task, task_in: schemas.TaskUpdate) -> models.Task:
    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()