from fastapi import FastAPI
# Importamos los routers desde la carpeta router (en singular, según tu estructura)
from app.router import tasks, projects

app = FastAPI(
    title="API de Gestión de Tareas y Proyectos",
    description="Práctica 1.3 - Organización con APIRouter"
)

# Puedes mantener tus endpoints de sistema (/health, /version, /ping) aquí 
# si no te han pedido moverlos, ya que no son de "negocio".
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

@app.get("/version", tags=["System"])
def get_version():
    return {"version": "1.0.0"}

@app.get("/ping", tags=["System"])
def ping():
    return {"ping": "pong"}

# Registramos los routers de negocio para que aparezcan en Swagger
app.include_router(tasks.router)
app.include_router(projects.router)