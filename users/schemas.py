from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# -------- User Schemas --------
class UserBase(BaseModel):
    name: str = Field(..., example="Pedro")
    mail: str = Field(..., example="pedro@gmail.com")
    telefono: Optional[str] = Field(None, example="987654321")
    usrdir: Optional[str] = Field(None, example="Av. Siempre Viva 123")
    rol: str = Field(..., example="user")
    fecha_creacion: Optional[date] = Field(None, example="2025-05-09")

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str = Field(..., example="Pedro")
    mail: str = Field(..., example="pedro@gmail.com")
    telefono: Optional[str] = Field(None, example="987654321")
    password: str = Field(..., example="supersegura123")
    usrdir: Optional[str] = Field(None, example="Av. Siempre Viva 123")
    fecha_creacion: Optional[date] = Field(None, example="2025-05-13")
    class Config:
        schema_extra = {
            "example": {
                "name": "Pedro",
                "mail": "pedro@gmail.com",
                "telefono": "987654321",
                "password": "supersegura123",
                "usrdir": "Av. Siempre Viva 123",
                "fecha_creacion": "2025-05-13"
            }
        }

class UserLogin(BaseModel):
    mail: str = Field(..., example="pedro@gmail.com")
    password: str = Field(..., example="supersegura123")

    class Config:
        schema_extra = {
            "example": {
                "mail": "pedro@gmail.com",
                "password": "supersegura123"
            }
        }

class User(UserBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Pedro",
                "mail": "pedro@gmail.com",
                "telefono": "987654321",
                "usrdir": "Av. Siempre Viva 123",
                "rol": "user",
                "fecha_creacion": "2025-05-09"
            }
        }

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Pedro")
    mail: Optional[str] = Field(None, example="pedro@gmail.com")
    telefono: Optional[str] = Field(None, example="987654321")
    usrdir: Optional[str] = Field(None, example="Av. Siempre Viva 123")
    rol: Optional[str] = Field(None, example="user")
    password: Optional[str] = Field(None, example="supersegura123")
    fecha_creacion: Optional[str] = Field(None, example="2025-05-09")

    class Config:
        schema_extra = {
            "example": {
                "name": "Pedro",
                "mail": "pedro@gmail.com",
                "telefono": "987654321",
                "usrdir": "Av. Siempre Viva 123",
                "rol": "user",
                "password": "supersegura123",
                "fecha_creacion": "2025-05-09"
            }
        }

# -------- Address Schemas --------
class AddressBase(BaseModel):
    direccion_: str = Field(..., example="Av. Siempre Viva 123")
    distrito: str = Field(..., example="Springfield")
    codigo_postal: Optional[str] = Field(None, example="12345")
    pais: str = Field(..., example="Perú")

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "direccion_": "Av. Siempre Viva 123",
                "distrito": "Springfield",
                "codigo_postal": "12345",
                "pais": "Perú"
            }
        }

class UserOut(User):
    pass