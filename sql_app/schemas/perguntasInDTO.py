from pydantic import BaseModel
from typing import Optional

class PerguntasInDTO(BaseModel):
    vaga: str
    link_descricao : str
    user_id: int
