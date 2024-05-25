# from typing import Union
# from pydantic import BaseModel
# from typing import Optional

# class UserBase(BaseModel):
#     nome: str
#     email: str
#     assinatura: str

#     model_config = {
#         "json_schema_extra": {
#             "examples": [
#                 {
#                     "nome": "João",
#                     "email": "joao@pessoal.com",
#                     "assinatura": "free"
                    
#                 }
#             ]
#         }
#     }


# class UserCreate(UserBase):
#     pass

# class User(UserBase):
#     id: int

#     class Config:
#         orm_mode = True


# class EntrevistaBase(BaseModel):
#     vaga: str
#     descricao: Optional[str] = None
#     link_perguntas: Optional[str] = None
#     link_avaliacao: Optional[str] = None
#     link_audio: Optional[str] = None
#     user_id: Optional[int] = None


# class EntrevistaCreate(EntrevistaBase):
#     pass

# class Entrevista(EntrevistaBase):
#     id: int

#     class Config:
#         orm_mode = True

