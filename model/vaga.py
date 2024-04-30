from pydantic import BaseModel
from typing import Optional

class Vaga(BaseModel):
    titulo: str
    descricao: str
    observacoes: str

    def to_text(self):
        return f"titulo: {self.titulo} descrição: {self.descricao} observações: {self.observacoes}"