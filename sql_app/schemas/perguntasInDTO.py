from pydantic import BaseModel
from typing import Optional

class PerguntasInDTO(BaseModel):
    vaga: str
    descricao : Optional[str] = None
