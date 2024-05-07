from pydantic import BaseModel
from typing import Optional

class EntrevistaInDTO(BaseModel):
    vaga: str
    descricao : Optional[str]