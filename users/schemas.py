from pydantic import BaseModel
from typing import Optional

# -------- User Schemas --------
class UserBase(BaseModel):
    name: str
    mail: str
    telefono: Optional[str] = None
    usrdir: Optional[str] = None
    rol: str
    fecha_creacion: Optional[str] = None

    class Config:
        from_attributes = True  # Para Pydantic v2

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    mail: str
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    mail: Optional[str] = None
    telefono: Optional[str] = None
    usrdir: Optional[str] = None
    rol: Optional[str] = None
    password: Optional[str] = None
    fecha_creacion: Optional[str] = None

# -------- Address Schemas --------
class AddressBase(BaseModel):
    direccion_: str
    distrito: str
    codigo_postal: Optional[str] = None
    pais: str

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    class Config:
        from_attributes = True

class UserOut(User):
    pass