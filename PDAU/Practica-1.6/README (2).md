# Práctica 1.6 - API RESTful de Gestión de Tareas

Este proyecto es una API RESTful desarrollada con **FastAPI** y **SQLAlchemy** (con SQLite como base de datos) para la gestión completa de Proyectos, Categorías y Tareas. 

El proyecto sigue una arquitectura modular en tres capas (Routers, Servicios y Schemas) para garantizar un código limpio, mantenible y escalable.

## 🛠️ Tecnologías Utilizadas
* **Framework:** FastAPI
* **ORM:** SQLAlchemy
* **Base de Datos:** SQLite (`taskflow.db`)
* **Validación de Datos:** Pydantic
* **Servidor ASGI:** Uvicorn

## 📂 Estructura del Proyecto
El código está organizado siguiendo el patrón de inyección de dependencias y separación de responsabilidades:
* `app/router/`: Controladores que definen los endpoints HTTP y manejan las peticiones/respuestas.
* `app/services/`: Capa de lógica de negocio y consultas directas a la base de datos con SQLAlchemy.
* `app/db/`: Configuración de la base de datos (`database.py`) y definición de las tablas (`models.py`).
* `app/schemas.py`: Modelos Pydantic para la validación y serialización de datos de entrada/salida.
* `app/main.py`: Punto de entrada de la aplicación, configuración de CORS y manejadores globales de errores.

## 🚀 Instalación y Ejecución

1. **Crear y activar entorno virtual:**
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/Mac:
   source .venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic
   ```

3. **Arrancar el servidor:**
   Ejecutar desde el directorio raíz del proyecto (donde se encuentra la carpeta `app`):
   ```bash
   uvicorn app.main:app --reload
   ```
   La API estará disponible en `http://127.0.0.1:8000` y la documentación interactiva (Swagger) en `http://127.0.0.1:8000/docs`.

## ⚙️ Justificación de Relaciones y Políticas de Borrado

De acuerdo con los requisitos de la práctica, se han implementado relaciones 1 a N entre las entidades. A continuación se justifican las decisiones tomadas para la integridad referencial en caso de borrado (`DELETE`):

### 1. Proyectos y Tareas (Borrado en Cascada - CASCADE)
* **Relación:** Un proyecto tiene múltiples tareas.
* **Decisión:** `ON DELETE CASCADE`.
* **Justificación:** Desde el punto de vista del negocio, una tarea pertenece intrínsecamente a un proyecto. Si un proyecto se cancela o se elimina del sistema, todas las tareas planificadas para ese proyecto dejan de tener sentido. Por lo tanto, al eliminar un registro en `projects`, la base de datos elimina automáticamente en cascada todas sus `tasks` asociadas para evitar mantener registros huérfanos e inútiles.

### 2. Categorías y Tareas (Anulación - SET NULL)
* **Relación:** Una categoría agrupa múltiples tareas.
* **Decisión:** `ON DELETE SET NULL`.
* **Justificación:** Las categorías actúan como etiquetas organizativas (ej. "Urgente", "Frontend", "Reunión"). Si se decide eliminar una categoría, las tareas que la tenían asignada siguen siendo válidas y necesitan completarse (el trabajo físico no desaparece por borrar su etiqueta). Por ello, al borrar un registro en `categories`, las tareas asociadas no se borran; simplemente su campo `category_id` pasa a ser `NULL`.

## 🧪 Pruebas (Colección de Postman)
El proyecto incluye un archivo JSON exportado con la colección completa de Postman. Esta colección contiene las 15 peticiones necesarias para probar todas las operaciones CRUD (Crear, Leer, Actualizar, Borrar) y los endpoints de resumen de estadísticas (`/summary`) para cada uno de los 3 recursos.