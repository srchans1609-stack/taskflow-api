from fastapi import APIRouter

# Configuración del router con su prefijo y etiqueta para Swagger
router = APIRouter(
    prefix="/tasks", # Para nivel Excelencia, puedes usar "/api/v1/tasks"
    tags=["tasks"]
)

# Fíjate que usamos @router en lugar de @app
@router.get("/")
def get_tasks():
    return {"message": "Obteniendo todas las tareas"}

@router.post("/")
def create_task():
    return {"message": "Creando una nueva tarea"}

@router.get("/")
def obtener_tareas():
    return [{"id": 1, "name": "Estudiar FastAPI"}]

# Cambiamos @app.post("/tasks") por @router.post("/")
@router.post("/")
def crear_tarea(tarea: dict):
    return {"message": "Tarea creada"}