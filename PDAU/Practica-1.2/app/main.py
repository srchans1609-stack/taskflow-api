from datetime import datetime
from fastapi import FastAPI, status
from pydantic import BaseModel, Field

# Importamos los schemas definidos en app/schemas.py
from app.schemas import TaskCreate, TaskRead

# Instancia principal de FastAPI
app = FastAPI(
    title="TaskFlow API",
    description="API RESTful para la gestión de tareas",
    version="1.0.0",
)


# --- Modelos de Respuesta del Sistema ---  
class HealthResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "ok"})


class VersionResponse(BaseModel):
    version: str = Field(..., json_schema_extra={"example": "1.0.0"})


class PingResponse(BaseModel):
    message: str = Field(..., json_schema_extra={"example": "pong"})


# --- Endpoints del Sistema ---
@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Estado de salud de la API",
    description="Devuelve el estado operativo de la aplicación.",
    tags=["System"],
)
def get_health():
    return {"status": "ok"}


@app.get(
    "/version",
    response_model=VersionResponse,
    summary="Versión de la aplicación",
    description="Devuelve la versión actual en ejecución.",
    tags=["System"],
)
def get_version():
    return {"version": "1.0.0"}


@app.get(
    "/ping",
    response_model=PingResponse,
    summary="Comprobación de conectividad",
    description="Endpoint rápido para verificar latencia y conectividad.",
    tags=["System"],
)
def get_ping():
    return {"message": "pong"}


# --- Endpoints de Tareas ---
@app.post(
    "/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva tarea (Endpoint Temporal)",
    description="Recibe un objeto TaskCreate, valida la entrada y devuelve un TaskRead simulado.",
    tags=["Tasks"],
)
def create_task(task_in: TaskCreate):
    """
    Crea una tarea simulada a partir de los datos recibidos en `TaskCreate`.
    """
    return TaskRead(
        id=1,
        title=task_in.title,
        description=task_in.description,
        project_id=task_in.project_id,
        completed=False,
        created_at=datetime.now(),
    ) 