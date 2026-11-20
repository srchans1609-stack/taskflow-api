# 📋 API de Gestión de Tareas - Práctica 1.6

Bienvenido al repositorio de la Práctica 1.6 - "TaskFlow". Esta API RESTful está construida con **FastAPI** y **SQLAlchemy**, y permite gestionar Proyectos, Tareas y Categorías de manera eficiente y escalable.

---

## Tecnologías Utilizadas

*   **Framework:** FastAPI
*   **Base de Datos:** SQLite (`taskflow.db`)
*   **ORM:** SQLAlchemy
*   **Validación de Datos:** Pydantic
*   **Servidor ASGI:** Uvicorn

---

## Arquitectura del Proyecto

El proyecto sigue una arquitectura en 3 capas (MVC/Router-Service-Repository) para garantizar la separación de responsabilidades:

1.  **Routers (`app/router/`)**: Gestionan exclusivamente las peticiones HTTP y la delegación de tareas.
2.  **Servicios (`app/services/`)**: Contienen toda la lógica de negocio y las consultas directas a la base de datos usando SQLAlchemy.
3.  **Esquemas (`app/schemas.py`)**: Validan los datos de entrada/salida mediante modelos de Pydantic.
4.  **Modelos de BD (`app/db/models.py`)**: Definen la estructura relacional de la base de datos.

---

## Justificación de Políticas de Borrado (Requisito de Evaluación)



### 1. Proyectos: Borrado en Cascada (`CASCADE`)
*   **Decisión:** Cuando se elimina un Proyecto, todas sus tareas asociadas se eliminan automáticamente.
*   **Código:** Implementado en `models.py` usando `ondelete="CASCADE"` en la clave foránea de la tabla `tasks` y `cascade="all, delete-orphan"` en la relación bidireccional del proyecto.


### 2. Categorías: Anulación del Enlace (`SET NULL`)
*   **Decisión:** Cuando se elimina una Categoría, las tareas asociadas no se borran; simplemente pierden su etiqueta de categoría (su campo `category_id` pasa a ser nulo).
*   **Código:** Implementado en `models.py` usando `ondelete="SET NULL"` en la clave foránea y permitiendo `nullable=True` en la columna.

---

## Guía de Instalación y Arranque
