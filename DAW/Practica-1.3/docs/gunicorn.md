# Práctica 1.3 - Instalación básica de Gunicorn

**Alumno:** Ander Chans Rodríguez
**Curso:** 2º DAW - IES Juan García Valdemora

## 1. Pasos ejecutados

Debido a que Gunicorn requiere dependencias exclusivas de sistemas UNIX  y no es compatible de forma nativa con Windows, la ejecución final del servidor se ha planteado sobre un entorno Linux (como una máquina virtual con Ubuntu Server). 

Los pasos seguidos han sido:
1. Creación del entorno virtual para aislar las dependencias del proyecto: `python3 -m venv venv`
2. Activación del entorno virtual: `source venv/bin/activate`
3. Integración de los archivos de la Práctica 1.1 (`main.py` dentro del directorio `app/` y el archivo `requirements.txt`).
4. Instalación de las dependencias requeridas y del servidor de aplicaciones:
   ```bash
   pip install -r requirements.txt
   pip install gunicorn
## 2. Evidencias de funcionamiento

A continuación se adjuntan las capturas de pantalla de la ejecución y verificación de los endpoints requeridos:

### Endpoint `/health`
![Verificación de Health](img/health.png)

### Endpoint `/ping`
![Verificación de Ping](img/ping.png)

### Endpoint `/version`
![Verificación de Version](img/version.png)

Como se observa en las respuestas, el servidor está devolviendo el JSON de nuestra API con código HTTP 200 y no la página HTML por defecto de un servidor web.