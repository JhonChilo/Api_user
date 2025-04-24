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

# ---------------- CREAR USUARIO ----------------
def create_user(db: Session, user: schemas.UserCreate):
    # Aseguramos que se proporciona una dirección
    if not user.address:
        raise HTTPException(status_code=400, detail="Address is required")

    # Asignación automática de rol
    role = "admin" if user.email in ADMIN_EMAILS else "user"  # Asigna admin si el correo está en la lista

    # Hashear la contraseña antes de guardarla
    hashed_password = hash_password(user.password)

    db_user = models.User(
        email=user.email,
        password=hashed_password,  # Guardamos la contraseña hasheada
        role=role
    )

    db_address = models.Address(
        country=user.address.country,
        city=user.address.city,
        street=user.address.street,
        postal_code=user.address.postal_code
    )

    db_user.address = db_address
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ---------------- LEER USUARIO ----------------
def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# ---------------- ACTUALIZAR USUARIO ----------------
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate, current_user_role: str):
    # Solo los administradores pueden cambiar el rol
    if user_update.role and current_user_role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to change user role")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.email:
        user.email = user_update.email
    if user_update.password:
        user.password = hash_password(user_update.password)  # Hashear la nueva contraseña
    if user_update.role:
        user.role = user_update.role

    if user_update.address:
        if user.address:
            user.address.country = user_update.address.country
            user.address.city = user_update.address.city
            user.address.street = user_update.address.street
            user.address.postal_code = user_update.address.postal_code
        else:
            user.address = models.Address(
                country=user_update.address.country,
                city=user_update.address.city,
                street=user_update.address.street,
                postal_code=user_update.address.postal_code
            )

    db.commit()
    db.refresh(user)
    return user

# ---------------- ELIMINAR USUARIO ----------------
def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
