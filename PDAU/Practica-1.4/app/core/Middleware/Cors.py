from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = [
    "http://localhost:5173"
]

def create_app() -> FastAPI:
    app = FastAPI(
        title="Mini Blog",
        description="API de blog con middleware y CORS"
    )

app.add_middleware(
      CORSMiddleware,
      allow_origins=ALLOWED_ORIGINS, 
      allow_credentials=True,
      allow_methods=ALLOWED_METHODS,  
      allow_headers=ALLOWED_HEADERS,
    )
