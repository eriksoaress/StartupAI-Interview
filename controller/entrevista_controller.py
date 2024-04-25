from fastapi import APIRouter,File, UploadFile
from PyPDF2 import PdfReader
import io
from service.entrevista_service import *
from model.vaga import *
from model.avaliacao import *
import io



entrevista_router = APIRouter( prefix="/entrevistas", tags=["entrevistas"])

@entrevista_router.post("/perguntas")
async def read_perguntas(vaga: Vaga, file: UploadFile = File(...)):
    conteudo_curriculo = await file.read()
    return get_perguntas(vaga.descricao, conteudo_curriculo)

@entrevista_router.post("/respostas")
def read_avaliacao(avaliacao: Avaliacao):
    return get_avaliacao(avaliacao.perguntas, avaliacao.respostas)

# @entrevista_router.post("/curriculo")
# async def read_curriculo(file: UploadFile = File(...)): 
#     contents = await file.read()

#     return {"text": text}