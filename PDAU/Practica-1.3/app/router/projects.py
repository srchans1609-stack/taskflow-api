from fastapi import APIRouter

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.get("/")
def get_projects():
    return [{"id": 1, "name": "Proyecto 1"}, {"id": 2, "name": "Proyecto 2"}]

@router.post("/")
def create_project(project: dict):
    return {"message": "Proyecto creado exitosamente", "data": project}