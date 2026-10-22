from fastapi import APIRouter

router = APIRouter(
    prefix="/projects", 
    tags=["Projects"],
)

@router.get("/")
def get_projects():
    return {"message": "Obteniendo todos los proyectos"}
# Cambiamos @app.get("/projects") por @router.get("/")

@router.get("/")
def obtener_proyectos():
    return [{"id": 1, "name": "Proyecto Modular"}]