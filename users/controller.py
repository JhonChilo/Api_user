from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import schemas, service
from .models import Address
from core.database import get_db  # Importa la función get_db

router = APIRouter()

# ---------------- CREAR USUARIO ----------------
@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, user)

# ---------------- LEER USUARIO ----------------
@router.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return service.get_user(db, user_id)

# ---------------- LEER TODOS LOS USUARIOS ----------------
@router.get("/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return service.get_users(db, skip, limit)

# ---------------- ACTUALIZAR USUARIO ----------------
@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    current_user_role = "admin"  # Este valor debería ser dinámico según el usuario autenticado
    return service.update_user(db, user_id, user_update, current_user_role)

# ---------------- ELIMINAR USUARIO ----------------
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return service.delete_user(db, user_id)
