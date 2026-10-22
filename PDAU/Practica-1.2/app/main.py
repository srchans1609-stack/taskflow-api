from fastapi import FastAPI
#Asegurarse de que la ruta de importación coincida con la estructura de carpetas del proyecto
from app.router import projects, tasks

app = FastAPI(
    title="TaskFlow API",
    description="API para la gestión de proyectos y tareas",
)


app.include_router(projects.router)
app.include_router(tasks.router)