from pydantic import BaseModel

class Pergunta(BaseModel):
    curriculo: str
    vaga: str
