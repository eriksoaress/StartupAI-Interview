from typing import Union
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    nome: str
    email: str
    assinatura: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "João",
                    "email": "joao@pessoal.com",
                    "assinatura": "free"
                    
                }
            ]
        }
    }


class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class EntrevistaBase(BaseModel):
    vaga: Optional[str]
    link_perguntas: Optional[str]
    link_respostas: Optional[str]
    link_avaliacao: Optional[str]
    link_audio: Optional[str]
    user_id: Optional[int]


class EntrevistaCreate(EntrevistaBase):
    pass

class Entrevista(EntrevistaBase):
    id: int

    class Config:
        orm_mode = True

