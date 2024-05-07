from fastapi import APIRouter,File, UploadFile
from PyPDF2 import PdfReader
import io
from service.entrevista_service import *
from model.vaga import *
from model.avaliacao import *
import io



entrevista_router = APIRouter( prefix="/entrevistas", tags=["entrevistas"])

@entrevista_router.post("/perguntas")
async def read_perguntas(vaga: str, file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return {"error": "Por favor, anexe um arquivo PDF"}
    contents = await file.read()
    return get_perguntas(vaga, contents)

@entrevista_router.post("/respostas")
def read_avaliacao(avaliacao: Avaliacao):
    return get_avaliacao(avaliacao.perguntas, avaliacao.respostas)

# @entrevista_router.post("/curriculo")
# async def read_curriculo(file: UploadFile = File(...)): 
#     contents = await file.read()

#     return {"text": text}