from fastapi import APIRouter
from pydantic import BaseModel, Field

# Crear el enrutador para el dominio del sistema
router = APIRouter()


class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")

class VersionResponse(BaseModel):
    version: str = Field(..., example="1.0.0")

class PingResponse(BaseModel):
    message: str = Field(..., example="pong")


# --- Endpoints ---
@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Estado de salud de la API",
    description="Devuelve el estado operativo de la aplicación.",
    tags=["System"]
)
def get_health():
    return {"status": "ok"}


@router.get(
    "/version",
    response_model=VersionResponse,
    summary="Versión de la aplicación",
    description="Devuelve la versión actual en ejecución.",
    tags=["System"]
)
def get_version():
    return {"version": "1.0.0"}


@router.get(
    "/ping",
    response_model=PingResponse,
    summary="Comprobación de conectividad",
    description="Endpoint rápido para verificar latencia y conectividad.",
    tags=["System"]
)
def get_ping():
    return {"message": "pong"}