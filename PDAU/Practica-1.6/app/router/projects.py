from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List  

from app.db.database import get_db
from app import schemas
from app.services import project_services

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

# Listar todos los proyectos con paginación
@router.get("/", response_model=List[schemas.ProjectRead])
def list_projects(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Límite por página"),
    db: Session = Depends(get_db)
):
    return project_services.get_all_projects(db, skip=skip, limit=limit)


# GET /projects/summary

@router.get("/summary")
def get_projects_summary(db: Session = Depends(get_db)):
    return project_services.get_projects_summary(db)



# GET /projects/{project_id} -> Detalle del proyecto

@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):    
    project = project_services.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Proyecto con ID {project_id} no encontrado"
        )
    return project



# Crear proyecto
@router.post("/", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return project_services.create_project(db, project_in)


 #Actualizar proyecto

@router.put("/{project_id}", response_model=schemas.ProjectRead)
def update_project(project_id: int, project_in: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = project_services.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Proyecto con ID {project_id} no encontrado"
        )
    return project_services.update_project(db, project, project_in)



#  Eliminar proyecto

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)): 
    project = project_services.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Proyecto con ID {project_id} no encontrado"
        )
    project_services.delete_project(db, project)
    return None