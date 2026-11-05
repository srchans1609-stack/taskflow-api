from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db import models
from app import schemas

def get_all_categories(db: Session, skip: int = 0, limit: int = 10) -> List[models.Category]:
    
    #Obtiene todas las categorías con paginación.
    
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category_by_id(db: Session, category_id: int) -> Optional[models.Category]:
    
    # Obtiene una categoría por su ID.
    # Se añade joinedload(models.Category.tasks) para que traiga
    # las tareas asociadas en la misma consulta (requisito explícito de la práctica).
    
    return (
        db.query(models.Category)
        .options(joinedload(models.Category.tasks))
        .filter(models.Category.id == category_id)
        .first()
    )

def get_categories_summary(db: Session) -> List[dict]:
    #
    # options(joinedload(...)): Carga las categorías y sus tareas vinculadas en una sola consulta SQL JOIN.
    # len(c.tasks): Calcula cuántas tareas tiene asignada cada categoría.
    
    categories = db.query(models.Category).options(joinedload(models.Category.tasks)).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "total_tasks": len(c.tasks)
        }
        for c in categories
    ]

def create_category(db: Session, category_in: schemas.CategoryCreate) -> models.Category:
    
    # Crea una nueva categoría.
    
    new_category = models.Category(**category_in.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def update_category(db: Session, category: models.Category, category_in: schemas.CategoryUpdate) -> models.Category:
    
    # Actualiza una categoría existente.
    
    update_data = category_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category: models.Category) -> None:
    
    # Elimina una categoría.
    
    db.delete(category)
    db.commit()