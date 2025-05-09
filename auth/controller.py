from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db  # Usamos get_db para obtener la sesión de base de datos
from users.models import User
from users.schemas import UserCreate, UserOut, UserLogin
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear contraseñas
def hash_password(password: str):
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(user_id: int):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"sub": user_id, "exp": expiration}, "your_secret_key", algorithm="HS256")  # Asegúrate de poner tu clave secreta en lugar de "your_secret_key"
    return token

ADMIN_EMAILS = ["jhon.chilo@utec.edu.pe", "sergio.delgado.a@utec.edu.pe"]

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.mail == user.mail).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(user.password)
        role = "admin" if user.mail in ADMIN_EMAILS else "user"

        new_user = User(
            name=user.name,
            mail=user.mail,
            telefono=user.telefono,
            usrdir=user.usrdir,
            rol=role,
            password=hashed_password,
            fecha_creacion=user.fecha_creacion
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Generar el token
        token = create_jwt_token(new_user.id)

        # Retornar id, token y datos del usuario
        return {
            "id": new_user.id,
            "name": new_user.name,
            "mail": new_user.mail,
            "telefono": new_user.telefono,
            "usrdir": new_user.usrdir,
            "rol": new_user.rol,
            "fecha_creacion": new_user.fecha_creacion,
            "token": token
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error: " + str(e))

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.mail == user.mail).first()
        if not db_user or not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_jwt_token(db_user.id)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error: " + str(e))
