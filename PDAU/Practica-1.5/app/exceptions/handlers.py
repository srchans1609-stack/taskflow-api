from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def create_app() -> FastAPI:
  app = FastAPI(title="Mini Blog", description="API con manejador global de errores")

  #Manejador global para cualquier excepción no controlada (Error 500)
  @app.exception_handler(Exception)
  async def global_exception_handler(request: Request, exc: Exception):
    # Aquí puedes hacer un print o usar logging para ver el error real en tu consola
    print(f"Error no controlado detectado: {exc}")

    # Retorna una respuesta JSON limpia sin exponer el stacktrace al cliente
    return JSONResponse(status_code=500, content={"error": "mensaje"})

  return app