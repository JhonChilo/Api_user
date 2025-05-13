from fastapi import APIRouter, Depends, HTTPException
import jwt
from sqlalchemy.orm import Session
from typing import List
from . import schemas, service, models
from .schemas import AddressCreate, Address
from core.database import get_db
from pydantic import BaseModel

router = APIRouter()

class MessageResponse(BaseModel):
    message: str

class TokenRequest(BaseModel):
    token: str
    usuario_id: int

@router.get("/addresses", response_model=List[Address])
def get_all_addresses(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    try:
        if page < 1 or size < 1:
            raise HTTPException(status_code=400, detail="Page and size must be greater than 0")
        skip = (page - 1) * size
        addresses = db.query(models.Address).offset(skip).limit(size).all()
        return addresses
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching addresses: " + str(e))

@router.get("/{usuario_id}", response_model=schemas.User)
def get_user(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return service.get_user(db, usuario_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching user: " + str(e))

@router.get("", response_model=List[schemas.User])
def get_users(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    try:
        if page < 1 or size < 1:
            raise HTTPException(status_code=400, detail="Page and size must be greater than 0")
        skip = (page - 1) * size
        return service.get_users(db, skip, size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching users: " + str(e))

@router.put("/{usuario_id}", response_model=schemas.User)
def update_user(usuario_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    try:
        current_user_role = "admin"  # Este valor debería ser dinámico según el usuario autenticado
        return service.update_user(db, usuario_id, user_update, current_user_role)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating user: " + str(e))

@router.delete("/{usuario_id}", response_model=MessageResponse)
def delete_user(usuario_id: int, db: Session = Depends(get_db)):
    try:
        service.delete_user(db, usuario_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting user: " + str(e))

@router.post("/{usuario_id}/address", response_model=Address)
def add_or_update_address(usuario_id: int, address_data: AddressCreate, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == usuario_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        address = db.query(models.Address).filter(models.Address.direccion_ == address_data.direccion_).first()
        if not address:
            address = models.Address(
                direccion_=address_data.direccion_,
                distrito=address_data.distrito,
                codigo_postal=address_data.codigo_postal,
                pais=address_data.pais
            )
            db.add(address)
            db.commit()
            db.refresh(address)
        user.usrdir = address.direccion_
        db.commit()
        db.refresh(user)
        return address
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error assigning address: " + str(e))

@router.put("/{usuario_id}/assign-address")
def assign_address(usuario_id: int, direccion: str, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == usuario_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        address = db.query(models.Address).filter(models.Address.direccion_ == direccion).first()
        if not address:
            address = models.Address(direccion_=direccion, distrito="Desconocido", codigo_postal=None, pais="Desconocido")
            db.add(address)
            db.commit()
            db.refresh(address)
        user.usrdir = direccion
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error assigning address: " + str(e))

@router.post("/verify-token")
def verify_token(body: TokenRequest):
    print(f"Verifying token: {body.token} for usuario_id: {body.usuario_id}")
    try:
        payload = jwt.decode(body.token, "72942250", algorithms=["HS256"])
        token_usuario_id = payload.get("usuario_id") or payload.get("sub")
        if str(token_usuario_id) != str(body.usuario_id):
            raise HTTPException(status_code=401, detail="El token no pertenece al usuario indicado")
        return {
            "valid": True,
            "usuario": token_usuario_id,
            "role": payload.get("role") or payload.get("rol")
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")