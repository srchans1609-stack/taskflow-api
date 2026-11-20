from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models import models
from app import schemas

def get_all_projects(db: Session, skip: int = 0, limit: int = 10) -> List[models.Project]:
    return db.query(models.Project).offset(skip).limit(limit).all()

def get_projects_summary(db: Session) -> List[dict]:
    projects = db.query(models.Project).options(joinedload(models.Project.tasks)).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "total_tasks": len(p.tasks),
            "completed_tasks": sum(1 for t in p.tasks if t.completed)
        }
        for p in projects
    ]

def get_project_by_id(db: Session, project_id: int) -> Optional[models.Project]:
    return db.query(models.Project).options(joinedload(models.Project.tasks)).filter(models.Project.id == project_id).first()

def create_project(db: Session, project_in: schemas.ProjectCreate) -> models.Project:
    new_project = models.Project(**project_in.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def update_project(db: Session, project: models.Project, project_in: schemas.ProjectUpdate) -> models.Project:
    update_data = project_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project: models.Project) -> None:
    db.delete(project)
    db.commit()