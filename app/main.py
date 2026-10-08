from fastapi import FastAPI

# Instancia principal de la aplicación FastAPI
app = FastAPI(
    title="TaskFlow API",
    description="API inicial para la práctica 1.1",
    version="1.0.0"
)

# Endpoint 1: Health
@app.get("/health", summary="Estado del servidor")
def get_health():
    return {"status": "ok"}

# Endpoint 2: Version
@app.get("/version", summary="Versión de la API")
def get_version():
    return {"version": "1.0.0"}

# Endpoint 3: Ping
@app.get("/ping", summary="Comprobación de conectividad")
def get_ping():
    return {"message": "pong"}