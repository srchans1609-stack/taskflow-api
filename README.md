# TaskFlow API — Práctica 1.1

API inicial para la gestión de tareas desarrollada con FastAPI.

## Arquitectura del Proyecto

Se ha optado por una estructura modular organizada en el paquete app/:

- app/main.py: Punto de entrada de la aplicación y configuración del servidor FastAPI.
(/health sirve para que te devuelva el estado, /version sirve para que te devuelva la versión, /ping que te devuelva la red).

## Requisitos e Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone [https://github.com/srchans1609-stack/taskflow-api.git](https://github.com/srchans1609-stack/taskflow-api.git)
   cd TaskFlow