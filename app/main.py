from fastapi import FastAPI
from app.api.router import router as api_router

# Instancia principal de FastAPI
app = FastAPI(
    title="TaskFlow API",
    description="API RESTful para la gestión de tareas (Práctica 1.1)",
    version="1.0.0",
)

# Incluir el enrutador modular por dominio
app.include_router(api_router)