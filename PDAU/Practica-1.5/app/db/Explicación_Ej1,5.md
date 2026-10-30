# Práctica 1.5 - Modelos SQLAlchemy y conexión a BD

## Objetivo de la Práctica
Persistir datos en una base de datos relacional (SQLite) utilizando el ORM SQLAlchemy en un proyecto estructurado con FastAPI.

## Archivos Creados y Modificados

### 1. `app/db/database.py`
Se encarga de la configuración del motor de la base de datos y la gestión de las sesiones.
- **Engine:** Configurado con `sqlite:///./taskflow.db` y `check_same_thread=False` para compatibilidad con FastAPI.
- **SessionLocal:** Creado con `expire_on_commit=False`.
- **Dependencia `get_db()`:** Inyecta la sesión de la BD en las peticiones. Utiliza un bloque `try/finally` junto con `yield` para asegurar que la conexión se cierra correctamente después de cada petición, evitando fugas de memoria.

### 2. `app/db/models.py`
Contiene el mapeo de las clases de Python a las tablas de la base de datos mediante el ORM de SQLAlchemy.
- Se definieron los modelos `User`, `Category`, `Project` y `Task`.
- **Relaciones :** `Task` tiene una FK obligatoria hacia `Project`.
- **Relaciones Bidireccionales:** Uso de `relationship` y `back_populates` para poder navegar entre entidades desde el código Python (ej. acceder a las tareas de un proyecto).
- **Cascade:** Configuración de `cascade="all, delete-orphan"` para mantener la integridad referencial (ej. si se borra un proyecto, se borran sus tareas asociadas).

### 3. Inyección en los Routers (`projects.py` y `tasks.py`)
- Se integro la base de datos en los endpoints usando la dependencia de FastAPI.
- Todos los endpoints de los routers incluyen ahora `db: Session = Depends(get_db)` como parámetro, asegurando que la conexión se abre y se cierra automáticamente en cada llamada HTTP.

## Errores que he tenido
- **Error con `pip freeze` y rutas rotas:** Se solucionó usando `python -m pip install -r requirements.txt` para forzar el uso del ejecutable del entorno virtual activo.
- **Error `ModuleNotFoundError: No module named 'app'` en Uvicorn:** Se corrigió ajustando el directorio en la terminal (ejecutando desde la carpeta que contiene `app/`) y usando la sintaxis correcta del módulo: `uvicorn app.main:app --reload`.
- **Error 404 en la ruta `/`:** Entendí que la ruta principal no estaba en el código, por lo que las pruebas debían hacerse directamente contra los endpoints configurados (como `/tasks`).