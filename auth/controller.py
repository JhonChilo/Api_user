from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from users.schemas import UserCreate, UserLogin
from .service import register_user, login_user

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = register_user(db, user)
        from .service import create_jwt_token  # Import aquí para evitar import circular si lo necesitas
        token = create_jwt_token(new_user.id, new_user.rol)
        return {
            "id": new_user.id,
            "name": new_user.name,
            "mail": new_user.mail,
            "rol": new_user.rol,
            "token": token
        }
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error inesperado: " + str(e))

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        return login_user(db, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error inesperado: " + str(e))