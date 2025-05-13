from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from users.schemas import UserCreate, UserLogin
from users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Correos que automáticamente tendrán rol admin
ADMIN_EMAILS = ["jhon.chilo@utec.edu.pe", "sergio.delgado.a@utec.edu.pe"]

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(usuario_id: int, rol: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode(
        {"usuario_id": usuario_id, "rol": rol, "exp": expiration},
        "72942250",
        algorithm="HS256"
    )
    return token

def register_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.mail == user.mail).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

        # Generar el siguiente id disponible
    last_user = db.query(User).order_by(User.id.desc()).first()
    next_id = (last_user.id + 1) if last_user else 1

    hashed_password = hash_password(user.password)
    role = "admin" if user.mail in ADMIN_EMAILS else "user"

    new_user = User(
        id=next_id,
        name=user.name,
        mail=user.mail,
        telefono=user.telefono,
        usrdir=user.usrdir,  # Puede ser None
        rol=role,
        password=hashed_password,
        fecha_creacion=user.fecha_creacion
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, user: UserLogin):
    db_user = db.query(User).filter(User.mail == user.mail).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token(db_user.id, db_user.rol)
    return {"access_token": token, "token_type": "bearer", "id": db_user.id, "rol": db_user.rol}