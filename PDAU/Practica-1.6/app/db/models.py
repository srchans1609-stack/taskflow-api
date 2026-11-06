from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    #Relación 1-N: Una categoría puede agrupar múltiples tareas
    tasks = relationship("Task", back_populates="category", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relación bidireccional con User
    owner = relationship("User", back_populates="projects")
    
    # Relación 1-N: Un proyecto tiene múltiples tareas
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    #FK  a Project requisito indispensable de la práctica
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True)

    #Relaciones bidireccionales, ES UN PUENTE QUE CONECTA LOS MODELOS
    project = relationship("Project", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")