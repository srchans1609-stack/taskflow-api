from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/")
def get_tasks():
    return [{"id": 1, "title": "Configurar APIRouter"}]

@router.post("/")
def create_task(task: dict):
    return {"message": "Tarea creada exitosamente", "data": task}