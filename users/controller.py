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

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return service.get_user(db, user_id)
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

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    try:
        current_user_role = "admin"  # Este valor debería ser dinámico según el usuario autenticado
        return service.update_user(db, user_id, user_update, current_user_role)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating user: " + str(e))

@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        service.delete_user(db, user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting user: " + str(e))

@router.post("/{user_id}/address", response_model=Address)
def add_or_update_address(user_id: int, address_data: AddressCreate, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
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

@router.get("/addresses/{address_id}", response_model=Address)
def get_address_by_id(address_id: str, db: Session = Depends(get_db)):
    try:
        address = db.query(models.Address).filter(models.Address.direccion_ == address_id).first()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        return address
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching address: " + str(e))

@router.put("/addresses/{address_id}", response_model=Address)
def update_address(address_id: str, address_update: AddressCreate, db: Session = Depends(get_db)):
    try:
        address = db.query(models.Address).filter(models.Address.direccion_ == address_id).first()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        for field, value in address_update.dict().items():
            setattr(address, field, value)
        db.commit()
        db.refresh(address)
        return address
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating address: " + str(e))

@router.delete("/addresses/{address_id}")
def delete_address(address_id: str, db: Session = Depends(get_db)):
    try:
        address = db.query(models.Address).filter(models.Address.direccion_ == address_id).first()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        db.delete(address)
        db.commit()
        return {"message": "Address deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting address: " + str(e))

@router.post("/verify-token")
def verify_token(token: str):
    print(f"Verifying token: {token}")
    try:
        payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        return {"valid": True, "user_id": payload.get("sub"), "role": payload.get("role")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.put("/{user_id}/assign-address")
def assign_address(user_id: int, direccion: str, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
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