from fastapi import APIRouter,File, UploadFile
from PyPDF2 import PdfReader
import io
from service.entrevista_service import *
from model.perguntas import *
from model.avaliacao import *
import uuid
import io
import pytesseract
from PIL import Image


entrevista_router = APIRouter( prefix="/entrevistas", tags=["entrevistas"])

@entrevista_router.post("/perguntas")
def read_perguntas(perguntas: Pergunta):
    return get_perguntas(perguntas.vaga, perguntas.curriculo)

@entrevista_router.post("/respostas")
def read_avaliacao(avaliacao: Avaliacao):
    return get_avaliacao(avaliacao.perguntas, avaliacao.respostas)

@entrevista_router.post("/curriculo")
async def read_curriculo(file: UploadFile = File(...)):
    contents = await file.read()

    
    # Lendo o arquivo PDF
    pdf_reader = PdfReader(io.BytesIO(contents))
    num_pages = len(pdf_reader.pages)
    text = ""

    # Iterando através de cada página do PDF e extraindo o texto
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    return {"text": text}