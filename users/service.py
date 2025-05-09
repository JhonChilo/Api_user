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
    # Si usrdir viene y no existe la dirección, la crea
    if user.usrdir:
        direccion = db.query(models.Address).filter(models.Address.direccion_ == user.usrdir).first()
        if not direccion:
            # Puedes ajustar estos valores por defecto según tu lógica o pedirlos en el registro
            nueva_direccion = models.Address(
                direccion_=user.usrdir,
                distrito="Desconocido",
                codigo_postal=None,
                pais="Desconocido"
            )
            db.add(nueva_direccion)
            db.commit()
            db.refresh(nueva_direccion)
    role = "admin" if user.mail in ADMIN_EMAILS else "user"
    hashed_password = hash_password(user.password)
    db_user = models.User(
        name=user.name,
        mail=user.mail,
        telefono=user.telefono,
        usrdir=user.usrdir,
        rol=role,
        password=hashed_password,
        fecha_creacion=user.fecha_creacion
    )
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
    try:
        return db.query(models.User).offset(skip).limit(limit).all()
    except Exception as e:
        print("ERROR EN get_users:", e)
        raise
# ---------------- ACTUALIZAR USUARIO ----------------
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate, current_user_role: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Solo actualiza los campos permitidos
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
def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
