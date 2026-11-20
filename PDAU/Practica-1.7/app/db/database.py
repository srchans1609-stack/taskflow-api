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
#El sessionLocal hace que al poner get_db se conecte a la base de datos y al terminar la petición se cierre la conexión automáticamente
#El autocommit esta en false para evitar que se guarde
#El bind conecta con el motor de la base de datos
#El expire evita que los objetos desaparezcan despues de un commit
#El base se pone para que se pueda crear la base de datos y las tablas
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    expire_on_commit=False
    )

Base = declarative_base()

#Dependencia get_db() con ciclo de vida gestionado por yield y try/finally para asegurar el cierre
#El db = SessionLocal crea una nueva sesion en la base de datos
#El yield db permite que la sesion se use para peticiones http
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()