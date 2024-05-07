# import openai
import openai
from openai import OpenAI
client = OpenAI()
from dotenv import load_dotenv
import os
import io
from PyPDF2 import PdfReader
from fastapi import APIRouter,File, UploadFile
from service.entrevista_service import *
from schemas import Entrevista, EntrevistaBase
from sqlalchemy.orm import Session
from models import *

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_perguntas(entrevista:EntrevistaBase, contents, db: Session):
    db_entrevista = EntrevistaModel(**entrevista.model_dump())
    # Lendo o arquivo PDF
    pdf_reader = PdfReader(io.BytesIO(contents))
    num_pages = len(pdf_reader.pages)
    curriculo = ""


    # Iterando através de cada página do PDF e extraindo o texto
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        curriculo += page.extract_text()

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "Você é um entrevistador conversando com um candidato a emprego com saída no formato JSON."},
        {"role": "user", "content": f"Me de exatamente 5 perguntas personalizadas e bem criativa para a vaga: {vaga}, com esse curriculo: {curriculo}, não envie o curriculo apenas as perguntas e envie-as no formato perguntanum : pergunta."}
    ],
    max_tokens=1000,
    temperature=0.9
    )
    db.add(db_entrevista)
    db.commit()

    return response.choices[0].message.content


def get_avaliacao(perguntas, respostas, db: Session):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "Você é um entrevistador conversando com um candidato a emprego com saída no formato JSON."},
        {"role": "user", "content": f"Considerando as perguntas:{perguntas} e as respostas:{respostas}, indique os pontos fortes e fracos da resposta das respostas, como o candidato poderia melhorar na próxima vez, e o que pode transmitir para o entrevistador essas respostas."}
    ],
    max_tokens=1000,
    temperature=0.9
    )
    return response.choices[0].message.content

