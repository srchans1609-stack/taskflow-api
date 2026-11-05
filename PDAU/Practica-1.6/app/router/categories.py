from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.db.database import get_db
from app.db import models
from app import schemas


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


#  GET /categories/ -> Listar categorías con paginación

# response_model=List[schemas.CategoryRead] asegura la serialización correcta con Pydantic.
@router.get("/", response_model=List[schemas.CategoryRead])
def list_categories(
    # skip: Cantidad de registros a omitir para cambiar de página
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    # limit: Cantidad máxima de registros a devolver por página
    limit: int = Query(10, ge=1, le=100, description="Límite de registros por página"),
    # db: Inyección de la sesión activa de SQLite
    db: Session = Depends(get_db)
):
    # db.query prepara la consulta a la tabla categories
    # .offset(skip).limit(limit) traduce la paginación a SQL
    # .all() ejecuta la consulta y devuelve los resultados en una lista
    return db.query(models.Category).offset(skip).limit(limit).all()





# FastAPI interpretará la palabra "summary" como si fuera un ID numérico y dará error 422
@router.get("/summary")
def get_categories_summary(db: Session = Depends(get_db)):
    # joinedload hace un JOIN para traer la categoría y sus tareas
    # Esto evita el problema de rendimiento "N+1 queries"
    categories = db.query(models.Category).options(joinedload(models.Category.tasks)).all()
    
    # Devuelve un listado ligero formateado con el contador total de tareas por categoría
    return [
        {
            "id": c.id,
            "name": c.name,
            "total_tasks": len(c.tasks)  # len() cuenta las tareas cargadas en la relación
        }
        for c in categories
    ]



# GET /categories/{id} -> Detalle de una categoría con sus tareas asociadas

@router.get("/{id}", response_model=schemas.CategoryRead)
def get_category(id: int, db: Session = Depends(get_db)):
    # Obtenemos la categoría especificada y traemos sus tareas anidadas vía joinedload 
    category = db.query(models.Category).options(joinedload(models.Category.tasks)).filter(models.Category.id == id).first()
    
    # Si no existe la categoría con dicho ID, se devuelve un error 404 explicito
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Categoría con ID {id} no encontrada"
        )
    return category



# POST /categories/ -> Crear una nueva categoría

# status_code=201 CREATED es el código HTTP estándar al registrar un nuevo recurso
@router.post("/", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category_in: schemas.CategoryCreate, db: Session = Depends(get_db)):
    # Comprobamos si ya existe una categoría con el mismo nombre en la base de datos
    existing = db.query(models.Category).filter(models.Category.name == category_in.name).first()
    if existing:
        # Si el nombre está duplicado, enviamos un 400 Bad Request para no romper la BD
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La categoría ya existe"
        )

    # category_in.model_dump() convierte el esquema Pydantic recibidó a un diccionario Python
   
    new_category = models.Category(**category_in.model_dump())
    
    db.add(new_category)      # Registra el nuevo objeto en la sesión de la BD
    db.commit()               # inserta la fila en la tabla SQL
    db.refresh(new_category)  # Recarga la entidad para obtener el 'id' autogenerado
    return new_category



# PUT /categories/{id} -> Editar una categoría existente

@router.put("/{id}", response_model=schemas.CategoryRead)
def update_category(id: int, category_in: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    # Buscamos la categoría existente.
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Categoría con ID {id} no encontrada"
        )

    # exclude_unset=True nos asegura que solo se modifiquen los campos que el cliente mandó en la petición
    update_data = category_in.model_dump(exclude_unset=True)
    
    # Bucle que asigna dinámicamente los nuevos valores a la categoría
    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()               # Guarda los cambios en la BD
    db.refresh(category)     # Recarga los datos actualizados
    return category



# status_code=204 NO CONTENT indica éxito al borrar y no devuelve nada en el body de respuesta
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Categoría con ID {id} no encontrada"
        )

   
    db.delete(category)       # Elimina el registro de la sesión
    db.commit()               # Aplica la eliminación en la base de datos
    return None