from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# class UserModel(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     nome = Column(String(50), nullable=False)
#     email = Column(String(50), nullable=False)
#     assinatura = Column(String(20), nullable=False)


