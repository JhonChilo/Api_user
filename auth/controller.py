from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db  # Usamos get_db para obtener la sesión de base de datos
from users.models import User
from users.schemas import UserCreate, UserOut, UserLogin
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear contraseñas
def hash_password(password: str):
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(user_id: int, rol: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode(
        {"user_id": user_id, "rol": rol, "exp": expiration},
        "72942250",
        algorithm="HS256"
    )
    return token

ADMIN_EMAILS = ["jhon.chilo@utec.edu.pe", "sergio.delgado.a@utec.edu.pe"]

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Validaciones de campos obligatorios y tipos
        if not isinstance(user.name, str) or not user.name.strip():
            raise HTTPException(status_code=422, detail="El campo 'name' es obligatorio y debe ser texto.")
        if not isinstance(user.mail, str) or "@" not in user.mail:
            raise HTTPException(status_code=422, detail="El campo 'mail' debe ser un correo válido.")
        if not isinstance(user.telefono, str) or not user.telefono.isdigit():
            raise HTTPException(status_code=422, detail="El campo 'telefono' debe ser numérico y obligatorio.")
        if not isinstance(user.password, str) or len(user.password) < 3:
            raise HTTPException(status_code=422, detail="El campo 'password' es obligatorio y debe tener al menos 3 caracteres.")

        db_user = db.query(User).filter(User.mail == user.mail).first()
        if db_user:
            raise HTTPException(status_code=400, detail="El correo ya está registrado.")

        last_user = db.query(User).order_by(User.id.desc()).first()
        next_id = 1 if last_user is None else last_user.id + 1

        hashed_password = hash_password(user.password)
        new_user = User(
            id=next_id,
            name=user.name,
            mail=user.mail,
            telefono=user.telefono,
            usrdir=None,
            rol="user",
            password=hashed_password,
            fecha_creacion=date.today()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_jwt_token(new_user.id, new_user.rol)

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
    except AttributeError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Error de atributo: {str(e)}. Verifica los nombres de los campos enviados.")
    except TypeError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Error de tipo de dato: {str(e)}. Verifica los tipos de los campos enviados.")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error de base de datos: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error inesperado: " + str(e))


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        if not isinstance(user.mail, str) or "@" not in user.mail:
            raise HTTPException(status_code=422, detail="El campo 'mail' debe ser un correo válido.")
        if not isinstance(user.password, str) or not user.password:
            raise HTTPException(status_code=422, detail="El campo 'password' es obligatorio.")

        db_user = db.query(User).filter(User.mail == user.mail).first()
        if not db_user:
            raise HTTPException(
                status_code=401,
                detail="El correo no está registrado.",
                headers={"X-Error-Type": "user_not_found"}
            )
        if not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=401,
                detail="La contraseña es incorrecta.",
                headers={"X-Error-Type": "wrong_password"}
            )
        token = create_jwt_token(db_user.id, db_user.rol)
        return {"access_token": token, "token_type": "bearer"}
    except AttributeError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Error de atributo: {str(e)}. Verifica los nombres de los campos enviados.",
            headers={"X-Error-Type": "attribute_error"}
        )
    except TypeError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Error de tipo de dato: {str(e)}. Verifica los tipos de los campos enviados.",
            headers={"X-Error-Type": "type_error"}
        )
    except HTTPException as e:
        # Permite que FastAPI maneje los HTTPException correctamente
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error inesperado: " + str(e),
            headers={"X-Error-Type": "unexpected_error"}
        )
# ...código existente...