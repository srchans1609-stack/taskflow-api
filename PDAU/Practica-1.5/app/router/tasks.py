from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    return [{"message": "GET tasks conectado a la BD"}]

@router.post("/")
def create_task(task: dict, db: Session = Depends(get_db)):
    return {"message": "POST task conectado a la BD", "data": task}

@router.get("/")
def get_tasks():
    return [{"id": 1, "title": "Configurar APIRouter"}]

@router.post("/")
def create_task(task: dict):
    return {"message": "Tarea creada exitosamente", "data": task}