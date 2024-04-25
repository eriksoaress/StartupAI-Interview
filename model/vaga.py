from pydantic import BaseModel
from typing import Optional

class Vaga(BaseModel):
    titulo: str
    descricao: str
    observacoes: str