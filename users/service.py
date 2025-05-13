from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
import bcrypt  

# Lista de correos de administradores
ADMIN_EMAILS = ["jhon.chilo@utec.edu.pe", "sergio.delgado.a@utec.edu.pe"]

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    # Generar un salt y luego hacer el hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def create_user(db: Session, user: schemas.UserCreate):
    try:
        # Obtener el siguiente id disponible
        last_user = db.query(models.User).order_by(models.User.id.desc()).first()
        next_id = (last_user.id + 1) if last_user else 1

        role = "admin" if user.mail in ADMIN_EMAILS else "user"
        hashed_password = hash_password(user.password)
        db_user = models.User(
            id=next_id,  # <-- Aquí asignas el id generado
            name=user.name,
            mail=user.mail,
            telefono=user.telefono,
            usrdir=user.usrdir,
            rol=role,
            password=hashed_password,
            fecha_creacion=user.fecha_creacion or date.today()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating user: " + str(e))

def get_user(db: Session, user_id: int):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching user: " + str(e))

def get_users(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.User).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching users: " + str(e))

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate, current_user_role: str):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user_update.name is not None:
            user.name = user_update.name
        if user_update.mail is not None:
            user.mail = user_update.mail
        if user_update.usrdir is not None:
            user.usrdir = user_update.usrdir
        if user_update.telefono is not None:
            user.telefono = user_update.telefono
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating user: " + str(e))

def delete_user(db: Session, user_id: int):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return {"detail": "User deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting user: " + str(e))