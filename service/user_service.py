from sqlalchemy.orm import Session
from ..repositories import user_repository
from ..schemas import user_schema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(db: Session, user_data: user_schema.UserCreate):
    if user_repository.get_by_email(db, user_data.email):
        raise ValueError("Email ya registrado")

    hashed_password = pwd_context.hash(user_data.password)
    new_user = user_schema.UserCreateDB(
        email=user_data.email, 
        hashed_password=hashed_password,
        role=user_data.role
    )
    return user_repository.save(db, new_user)
