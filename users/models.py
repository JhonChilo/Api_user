from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Address(Base):
    __tablename__ = "direccion"

    direccion_ = Column(String(255), primary_key=True, index=True)
    distrito = Column(String(100), nullable=False)
    codigo_postal = Column(String(20), nullable=True)
    pais = Column(String(100), nullable=False)

    users = relationship("User", back_populates="address")

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    mail = Column(String(255), unique=True, index=True, nullable=False)
    telefono = Column(String(255), nullable=True)
    usrdir = Column(String(255), ForeignKey("direccion.direccion_"), nullable=True)
    rol = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    fecha_creacion = Column(String, nullable=True)  # O usa Date si lo prefieres

    address = relationship("Address", back_populates="users", uselist=False)