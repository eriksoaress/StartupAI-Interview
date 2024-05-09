# import openai
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import io
from PyPDF2 import PdfReader
from services.entrevista_service import *
from schemas_ import Entrevista, EntrevistaBase
from sqlalchemy.orm import Session
from models import *
from database import get_db
from sql_app.dtos.perguntasInDTO import PerguntasInDTO

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def get_perguntas(entrevista:PerguntasInDTO, contents, db: Session):
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
        {"role": "system", "content": "Você é um entrevistador entrevistando um candidato a emprego com saída no formato JSON."},
        {"role": "user", "content": f"Me de exatamente 3 perguntas personalizadas para a vaga: {entrevista.vaga} com a seguinte descrição: {entrevista.descricao}, com esse curriculo: {curriculo}, envie-as no formato 'pergunta(numero) : pergunta'."}
    ],
    max_tokens=1000,
    temperature=0.9
    )
    db_entrevista.link_perguntas = response.choices[0].message.content
    db.add(db_entrevista)
    db.commit()

    return response.choices[0].message.content


def get_avaliacao(entrevista_id: str, respostas: str, db: Session):
    perguntas = db.query(EntrevistaModel.link_perguntas).filter(EntrevistaModel.id == entrevista_id).first()
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "Você é um entrevistador entrevistando um candidato a emprego com saída no formato JSON."},
        {"role": "user", "content": f"Considerando as perguntas:{perguntas} e as respostas:{respostas}, forneça um feedback no formato: pontos fortes: Destaque os pontos fortes da resposta do candidato para que ele saiiba o que fez de bom. pontos fracos: Destaque os pontos fracos da resposta do candidato para que ele saiba o que precisa melhorar."}
    ],
    max_tokens=1000,
    temperature=0.9
    )
    return response.choices[0].message.content