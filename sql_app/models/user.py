from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from schemas.roles import Roles

from database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(75), nullable=False)
    email = Column(String(75), nullable=False,unique=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False)
    role = Column(Enum(Roles), nullable=False)
    
    entrevistas = relationship("EntrevistaModel", back_populates="user")