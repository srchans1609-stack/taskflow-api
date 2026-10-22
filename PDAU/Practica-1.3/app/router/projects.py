from fastapi import APIRouter

# Instanciamos el router con su prefijo y etiqueta
router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

# Endpoint GET para obtener proyectos
@router.get("/")
def get_projects():
    return [{"id": 1, "name": "Proyecto 1"}, {"id": 2, "name": "Proyecto 2"}]

# Endpoint POST para crear un proyecto (opcional, pero útil para la práctica)
@router.post("/")
def create_project(project: dict):
    return {"message": "Proyecto creado exitosamente", "data": project}