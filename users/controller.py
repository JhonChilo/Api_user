from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import schemas, service, models
from .schemas import AddressCreate, Address
from core.database import get_db

router = APIRouter()

# ---------------- LEER USUARIO ----------------
@router.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return service.get_user(db, user_id)

# ---------------- LEER TODOS LOS USUARIOS ----------------
@router.get("/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return service.get_users(db, skip, limit)

@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    current_user_role = "admin"  # Este valor debería ser dinámico según el usuario autenticado
    return service.update_user(db, user_id, user_update, current_user_role)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return service.delete_user(db, user_id)

# ---------------- AÑADIR O ACTUALIZAR DIRECCIÓN ----------------
@router.post("/users/{user_id}/address", response_model=Address)
def add_or_update_address(user_id: int, address_data: AddressCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_address = db.query(models.Address).filter(models.Address.user_id == user_id).first()
    if existing_address:
        existing_address.street = address_data.street
        existing_address.city = address_data.city
        existing_address.country = address_data.country
        existing_address.postal_code = address_data.postal_code
    else:
        new_address = models.Address(
            user_id=user_id,
            street=address_data.street,
            city=address_data.city,
            country=address_data.country,
            postal_code=address_data.postal_code
        )
        db.add(new_address)

    db.commit()
    db.refresh(existing_address if existing_address else new_address)

    return existing_address if existing_address else new_address
