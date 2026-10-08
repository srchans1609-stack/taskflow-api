from fastapi import FastAPI
from pydantic import BaseModel, Field

# Instancia principal de FastAPI
app = FastAPI(
    title="TaskFlow API",
    description="API RESTful para la gestión de tareas (Práctica 1.1)",
    version="1.0.0",
)


# --- Modelos de Respuesta (Pydantic) ---
class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")


class VersionResponse(BaseModel):
    version: str = Field(..., example="1.0.0")


class PingResponse(BaseModel):
    message: str = Field(..., example="pong")


# --- Endpoints ---
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
    