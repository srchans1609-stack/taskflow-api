from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    return [{"message": "GET projects conectado a la BD"}]

@router.post("/")
def create_project(project: dict, db: Session = Depends(get_db)):
    return {"message": "POST project conectado a la BD", "data": project}

@router.get("/")
def get_projects():
    return [{"id": 1, "name": "Proyecto 1"}, {"id": 2, "name": "Proyecto 2"}]

@router.post("/")
def create_project(project: dict):
    return {"message": "Proyecto creado exitosamente", "data": project}