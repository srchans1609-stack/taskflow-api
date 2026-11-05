from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app import schemas
from app.services import categories_services

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# GET /categories/ -> Listar categorías paginadas

@router.get("/", response_model=List[schemas.CategoryRead])
def list_categories(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Límite por página"),
    db: Session = Depends(get_db)
):
    return categories_services.get_all_categories(db, skip=skip, limit=limit)



# GET /categories/summary 

@router.get("/summary")
def get_categories_summary(db: Session = Depends(get_db)):
    return categories_services.get_categories_summary(db)



# Detalle de categoría con sus tareas

@router.get("/{category_id}", response_model=schemas.CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = categories_services.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {category_id} no encontrada"
        )
    return category


# Crear categoría
@router.post("/", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category_in: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return categories_services.create_category(db, category_in)



# Editar categoría
@router.put("/{category_id}", response_model=schemas.CategoryRead)
def update_category(
    category_id: int, 
    category_in: schemas.CategoryUpdate, 
    db: Session = Depends(get_db)
):
    category = categories_services.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {category_id} no encontrada"
        )
    return categories_services.update_category(db, category, category_in)



# Eliminar categoría
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = categories_services.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {category_id} no encontrada"
        )

    categories_services.delete_category(db, category)
    return None