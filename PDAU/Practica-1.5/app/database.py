from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Configuración del engine con SQLite
#check_same_thread=False permite que la conexión sea compartida entre hilos
SQLALCHEMY_DATABASE_URL = "sqlite:///./taskflow.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#Se define expire_on_commit=False para que los objetos no se expiren después de un commit
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    expire_on_commit=False
    )

Base = declarative_base()

#Dependencia get_db() con ciclo de vida gestionado por yield y try/finally para asegurar el cierre
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()