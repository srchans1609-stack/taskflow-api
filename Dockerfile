# 1. Imagen base ligera de Python
FROM python:3.11-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de dependencias
COPY requirements.txt .

# 4. Instalar las dependencias de FastAPI
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el código fuente (tu archivo main.py)
COPY . .

# 6. Exponer el puerto por defecto de FastAPI (8000)
EXPOSE 8000

# 7. Comando para arrancar la API con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]