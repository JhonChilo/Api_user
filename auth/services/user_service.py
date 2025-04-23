from sqlalchemy.orm import Session
from app.auth.models.user import User
from app.auth.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    def create_user(self, db: Session, user: UserCreate):
        db_user = User(username=user.username, email=user.email, 
                       hashed_password=get_password_hash(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            if user_update.username:
                db_user.username = user_update.username
            if user_update.email:
                db_user.email = user_update.email
            if user_update.password:
                db_user.hashed_password = get_password_hash(user_update.password)
            db.commit()
            db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user
