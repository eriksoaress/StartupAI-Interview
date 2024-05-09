from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class UserModelTest(Base):
    __tablename__ = "user_test"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)