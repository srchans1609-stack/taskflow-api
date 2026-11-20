from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)  # "user" o "admin"
    refresh_token = Column(String, nullable=True)

    # Relación bidireccional con Project (necesaria por back_populates="projects" en models.py)
    projects = relationship("Project", back_populates="owner")