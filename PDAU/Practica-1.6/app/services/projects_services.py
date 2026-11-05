from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db import models
from app import schemas


# Obtener todos los proyectos 

def get_all_projects(db: Session, skip: int = 0, limit: int = 10) -> List[models.Project]:
    
    #  db.query(models.Project): Indica a SQLAlchemy que trabajaremos sobre la tabla projects
    #  .limit(limit): Trae como máximo de registros
    #  .all(): Ejecuta la orden en SQL y devuelve una lista de objetos Project
   
    return db.query(models.Project).offset(skip).limit(limit).all()



# Obtener resumen/estadísticas de proyectos (Criterio "Excelente")

def get_projects_summary(db: Session) -> List[dict]:
    
    # Esto trae cada proyecto junto con sus tareas en 1 sola consulta a la BD 
    # sum(1 for t in p.tasks if t.completed): Recorre las tareas cargadas en memoria y cuenta cuántas tienen completed=True
    
    projects = db.query(models.Project).options(joinedload(models.Project.tasks)).all()
    
    return [
        {
            "id": p.id,
            "name": p.name,
            "total_tasks": len(p.tasks),                              # Cuenta el total de tareas asignadas
            "completed_tasks": sum(1 for t in p.tasks if t.completed) # Cuenta solo las tareas finalizadas
        }
        for p in projects
    ]



# Obtener detalle de un proyecto por ID

def get_project_by_id(db: Session, project_id: int) -> Optional[models.Project]:
    
    # joinedload: Trae las tareas del proyecto para cumplir el requisito de la respuesta anidada.
    # .filter(): Aplica la cláusula WHERE en la consulta.
    # .first(): Devuelve el primer resultado encontrado o None si el proyecto no existe.
    
    return db.query(models.Project).options(joinedload(models.Project.tasks)).filter(models.Project.id == project_id).first()



# Crear un nuevo proyecto

def create_project(db: Session, project_in: schemas.ProjectCreate) -> models.Project:
    
    # project_in.model_dump(): Convierte el esquema Pydantic a diccionario.
    # **... : Desempaqueta las claves como argumentos del modelo de BD
    # db.commit(): Confirma la transacción e inserta la fila
    # db.refresh(): Recarga la instancia desde la BD para asignarle el id
    
    new_project = models.Project(**project_in.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project



# Actualizar un proyecto existente

def update_project(db: Session, project: models.Project, project_in: schemas.ProjectUpdate) -> models.Project:
   
    #exclude_unset=True: Extrae solo los campos que el usuario envió explícitamente en el 
    #Si solo envía {"name": "Nuevo Nombre"}, ignora description para no ponerlo en None por error
    # setattr(project, key, value): Asigna el nuevo valor a la propiedad del objeto ORM en memoria
    # db.refresh(): Recarga el objeto para asegurar que devuelva los datos actualizados
    
    update_data = project_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
        
    db.commit()
    db.refresh(project)
    return project



# Eliminar un proyecto

def delete_project(db: Session, project: models.Project) -> None:
    
    
    db.delete(project)
    db.commit()