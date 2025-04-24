from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(String(50), nullable=False)

    address = relationship("Address", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    street = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=True)

    user = relationship("User", back_populates="address")
