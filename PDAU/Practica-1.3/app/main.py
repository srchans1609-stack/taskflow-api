from fastapi import FastAPI
from app.router import tasks, projects

app = FastAPI(
    title="API de Gestión de Tareas y Proyectos",
    description="Práctica 1.3 - Organización con APIRouter"
)

# Endpoints de sistema
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

@app.get("/version", tags=["System"])
def get_version():
    return {"version": "1.0.0"}

@app.get("/ping", tags=["System"])
def ping():
    return {"ping": "pong"}

# Inclusión de los routers de negocio
app.include_router(tasks.router)
app.include_router(projects.router)