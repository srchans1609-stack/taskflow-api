# TaskFlow API - Autenticación y Seguridad JWT (Práctica 1.7)

API RESTful desarrollada con FastAPI y SQLAlchemy para la gestión de proyectos, tareas y categorías, protegida mediante autenticación basada en JSON Web Tokens (JWT) y control de acceso por roles (scopes).

## Arquitectura del Proyecto

```text
TaskFlow/
├── app/
│   ├── core/
│   │   └── security.py         # Hashing bcrypt, emisión/validación JWT y dependencias OAuth2
│   ├── db/
│   │   ├── database.py         # Conexión y sesión SQLAlchemy
│   │   └── models.py           # Modelos ORM (User, Project, Task, Category)
│   ├── routers/
│   │   ├── auth.py             # Endpoints /auth/register, /auth/login y /auth/refresh
│   │   ├── categories.py       # Endpoints CRUD de categorías
│   │   ├── projects.py         # Endpoints CRUD de proyectos (escritura protegida por scope)
│   │   └── tasks.py            # Endpoints CRUD de tareas (escritura protegida por scope)
│   ├── schemas/
│   │   └── auth.py             # Esquemas Pydantic para usuarios y tokens
│   ├── services/
│   │   ├── auth_service.py     # Lógica de registro, autenticación y rotación de tokens
│   │   ├── categories_services.py
│   │   ├── project_services.py
│   │   └── tasks_services.py
│   └── main.py                 # Punto de entrada de la aplicación FastAPI
└── requirements.txt