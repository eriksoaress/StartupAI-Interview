from pydantic import BaseModel

class Avaliacao(BaseModel):
    perguntas: str
    respostas: str
