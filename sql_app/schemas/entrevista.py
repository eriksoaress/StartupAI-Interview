from pydantic import BaseModel
from typing import Optional

class EntrevistaBase(BaseModel):
    vaga: str
    descricao: Optional[str] = None
    link_perguntas: Optional[str] = None
    link_avaliacao: Optional[str] = None
    link_audio: Optional[str] = None
    user_id: Optional[int] = None


class EntrevistaCreate(EntrevistaBase):
    pass

class Entrevista(EntrevistaBase):
    id: int

    class Config:
        orm_mode = True