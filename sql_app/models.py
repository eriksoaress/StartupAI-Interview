from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    assinatura = Column(String(20), nullable=False)
    entrevistas = relationship("EntrevistaModel", back_populates="user")

class EntrevistaModel(Base):
    __tablename__ = "entrevistas"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    vaga = Column(String(50), nullable=False)
    descricao = Column(String(250), nullable=True)
    link_perguntas = Column(String(250), nullable=True)
    link_avaliacao = Column(String(250), nullable=True)
    link_audio = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("UserModel", back_populates="entrevistas")