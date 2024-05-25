from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class EntrevistaModel(Base):
    __tablename__ = "entrevistas"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    vaga = Column(String(50), nullable=False)
    link_descricao = Column(String(250), nullable=True)
    link_perguntas = Column(String(250), nullable=True)
    link_avaliacao = Column(String(250), nullable=True)
    link_audio = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("UserModel", back_populates="entrevistas")