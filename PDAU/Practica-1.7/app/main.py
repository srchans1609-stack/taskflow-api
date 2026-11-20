import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
from app.models import models, user
from app.router import auth, tasks, projects, categories

# Crea las tablas en la BD automáticamente si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión de Tareas, Proyectos y Categorías",
    description="Práctica 1.7 - Autenticación JWT"
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
    response.headers["X-Process-Time"] = str(process_time * 1000)
    return response

# 3. Manejador global de excepciones 
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Error interno del servidor"}
    )

# Endpoints de sistema
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

@app.get("/version", tags=["System"])
def get_version():
    return {"version": "1.7.0"}

@app.get("/ping", tags=["System"])
def ping():
    return {"ping": "pong"}

# Inclusión de los routers de negocio y autenticación
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(projects.router)
app.include_router(categories.router)