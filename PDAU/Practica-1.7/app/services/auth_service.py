from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.models.user import User
from app.schemas import UserCreate
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM,
)

def get_scopes_by_role(role: str) -> list[str]:
    if role == "admin":
        return ["tasks:write", "projects:write"]
    return ["tasks:write"]

def register_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario no está disponible",
        )

    new_user = User(
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role if user_data.role in ["user", "admin"] else "user",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str) -> dict:
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scopes = get_scopes_by_role(user.role)
    access_token = create_access_token(data={"sub": user.username, "scopes": scopes})
    refresh_token = create_refresh_token(data={"sub": user.username, "scopes": scopes})

    user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

def rotate_refresh_token(db: Session, refresh_token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        if username is None or token_type != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if not user or user.refresh_token != refresh_token:
        raise credentials_exception

    scopes = get_scopes_by_role(user.role)
    new_access_token = create_access_token(data={"sub": user.username, "scopes": scopes})
    new_refresh_token = create_refresh_token(data={"sub": user.username, "scopes": scopes})

    user.refresh_token = new_refresh_token
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }