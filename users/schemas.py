from pydantic import BaseModel
from typing import Optional

# -------- Address Schemas --------
class AddressBase(BaseModel):
    country: str
    city: str
    street: str
    postal_code: Optional[str] = None

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# -------- User Schemas --------
class UserBase(BaseModel):
    email: str

class UserCreate(BaseModel):  # No incluye `role` porque se asignará en el backend
    email: str
    password: str
    address: AddressCreate
    username: str

class User(UserBase):
    id: int
    role: str  # El rol será asignado automáticamente por el backend
    address: Address

    class Config:
        orm_mode = True

class UserOut(UserBase):
    id: int
    role: str
    address: Address

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    address: Optional[AddressCreate] = None
