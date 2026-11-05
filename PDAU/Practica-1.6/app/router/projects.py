from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

# GET /projects/ -> Listar todos los proyectos con paginación

# response_model=List[schemas.ProjectRead] valida que se devuelvan objetos formateados según Pydantic
@router.get("/", response_model=List[schemas.ProjectRead])
def list_projects(
    # skip: número de registros a omitir 
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    # limit: número máximo de registros a traer 
    limit: int = Query(10, ge=1, le=100, description="Límite por página"),
    # db: Inyección de la sesión activa de la base de datos.
    db: Session = Depends(get_db)
):
    # Traduce la paginación a SQL mediante OFFSET (skip) y LIMIT (limit)
    return db.query(models.Project).offset(skip).limit(limit).all()



# GET /projects/summary -> Devuelve un resumen de todos los proyectos con estadísticas de tareas


@router.get("/summary")
def get_projects_summary(db: Session = Depends(get_db)):
    # joinedload realiza un JOIN en SQL para traer el proyecto y sus tareas asociadas en una sola consulta.
    projects = db.query(models.Project).options(joinedload(models.Project.tasks)).all()
    
    # Devuelve un listado con total de tareas y tareas completadas
    return [
        {
            "id": p.id,
            "name": p.name,
            "total_tasks": len(p.tasks),
            "completed_tasks": sum(1 for t in p.tasks if t.completed)
        }
        for p in projects
    ]



# GET /projects/{id} -> Detalle de un proyecto con sus tareas anidadas

@router.get("/{id}", response_model=schemas.ProjectRead)
def get_project(id: int, db: Session = Depends(get_db)):
    # joinedload trae automáticamente las tareas vinculadas al proyecto para cumplir el contrato REST de la práctica
    project = db.query(models.Project).options(joinedload(models.Project.tasks)).filter(models.Project.id == id).first()
    
    # Si el proyecto no existe en la BD, devolvemos un error 404 
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Proyecto con ID {id} no encontrado"
        )
    return project



# POST /projects/ -> Crear un nuevo proyecto

# status_code=201 CREATED es el estándar HTTP al guardar un nuevo recurso
@router.post("/", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # project_in.model_dump() convierte el objeto Pydantic enviado en el body a un diccionario.
    # El operador ** desempaqueta 'name' y 'description' dentro del modelo de SQLAlchemy.
    new_project = models.Project(**project_in.model_dump())
    
    db.add(new_project)      # Añade la entidad a la sesión
    db.commit()               # Ejecuta el INSERT en SQLite
    db.refresh(new_project)  # Recarga la entidad para obtener el 'id' asignado por la BD
    return new_project



# PUT /projects/{id} -> Editar un proyecto existente

@router.put("/{id}", response_model=schemas.ProjectRead)
def update_project(id: int, project_in: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Proyecto con ID {id} no encontrado"
        )

    # exclude_unset=True evita sobrescribir campos con None si el cliente solo envía un campo a actualizar
    update_data = project_in.model_dump(exclude_unset=True)
    
    # Asigna dinámicamente cada campo actualizado en la entidad
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()               # Guarda los cambios.
    db.refresh(project)      # Obtiene los datos actualizados.
    return project



# DELETE /projects/{id} -> Eliminar un proyecto

# status_code=204 NO CONTENT confirma el borrado exitoso sin devolver nada en el body
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Proyecto con ID {id} no encontrado"
        )

    
    
    db.delete(project)
    db.commit()
    return None