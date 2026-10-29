import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.router import tasks, projects

app = FastAPI(
    title="API de Gestión de Tareas y Proyectos",
    description="Práctica 1.4 - Middleware, CORS y Manejo de Errores"
)

# 1. Configuración de CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Middleware personalizado para añadir la cabecera X-Process-Time en milisegundos
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    # Se convierte a milisegundos y se asigna a la cabecera
    response.headers["X-Process-Time"] = str(process_time * 1000)
    return response

# 3. Manejador global de excepciones 
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "mensaje"}
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