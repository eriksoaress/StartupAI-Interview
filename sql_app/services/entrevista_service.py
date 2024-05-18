import openai
import boto3
from openai import OpenAI
from dotenv import load_dotenv
import os
import io
from PyPDF2 import PdfReader
from services.entrevista_service import *
from sqlalchemy.orm import Session
from models import *
from database import get_db
from schemas.perguntasInDTO import PerguntasInDTO
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from models_ import *
import uuid
from fastapi import UploadFile



load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DG_API_KEY = os.getenv("DG_API_KEY")
client = OpenAI()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))


async def transc_audio(audio_file: UploadFile, db: Session):
    try:
        deepgram = DeepgramClient(DG_API_KEY)
        buffer_data = await audio_file.read()  # Lê o conteúdo do arquivo
        payload: FileSource = {
            "buffer": buffer_data,
        }
        options = {
            "punctuate": True,
            "model": "nova-2",
            "detect_language": True
        }
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        return response.results.channels[0].alternatives[0].transcript

    except Exception as e:
        return f"Exception: {e}"


def cria_arquivo_perguntas(mensagem, id_entrevista):
    nome_arquivo = f'perguntas_{id_entrevista}.txt'
    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        file.write(mensagem)
    bucket_name = 'pontochaveai'
    s3_client.upload_file(nome_arquivo, bucket_name, nome_arquivo)
    os.remove(nome_arquivo)
    return 

def cria_arquivo_avaliacao(mensagem, id_entrevista):
    nome_arquivo = f'avaliacao_{id_entrevista}.txt'
    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        file.write(mensagem)
    bucket_name = 'pontochaveai'
    s3_client.upload_file(nome_arquivo, bucket_name, nome_arquivo)
    os.remove(nome_arquivo)
    return

def cria_arquivo_respostas(mensagem, id_entrevista):
    nome_arquivo = f'respostas_{id_entrevista}.txt'
    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        file.write(mensagem)
    bucket_name = 'pontochaveai'
    s3_client.upload_file(nome_arquivo, bucket_name, nome_arquivo)
    os.remove(nome_arquivo)
    return

def cria_arquivo_descricao(mensagem, id_entrevista):
    nome_arquivo = f'descricao_{id_entrevista}.txt'
    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        file.write(mensagem)
    bucket_name = 'pontochaveai'
    s3_client.upload_file(nome_arquivo, bucket_name, nome_arquivo)
    os.remove(nome_arquivo)
    return

def get_text_from_s3(link):
    bucket_name = 'pontochaveai'
    file_name = link.split('/')[-1]
    s3_client.download_file(bucket_name, file_name, file_name)
    with open(file_name, 'r') as file:
        text = file.read()
    os.remove(file_name)
    return text



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
    model="gpt-4o",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "Você é um entrevistador entrevistando um candidato a emprego com saída no formato JSON."},
        {"role": "user", "content": "Me de exatamente 6 perguntas personalizadas para a vaga: "+entrevista.vaga+" com a seguinte descrição: "+entrevista.link_descricao+", com esse curriculo (considere apenas as coisas do curriculo que são relevantes para a área, senão pode fazer perguntas relacionados a valores da empresa, coisas que não estão no curriculo, história de vida, etc): "+curriculo+", envie-as no seguinte formato {'pergunta(numero)': 'pergunta'}."}
    ],
    max_tokens=1000,
    temperature=0.9
    )

    # pega o proximo id da tabela e cria o arquivo de perguntas com o id
    uuid_ = uuid.uuid4()
    cria_arquivo_perguntas(response.choices[0].message.content, uuid_)
    cria_arquivo_descricao(entrevista.link_descricao, uuid_)
    db_entrevista.link_perguntas = f'https://pontochaveai.s3.amazonaws.com/perguntas_{uuid_}.txt'
    db_entrevista.link_descricao = f'https://pontochaveai.s3.amazonaws.com/descricao_{uuid_}.txt'
    db.add(db_entrevista)
    db.commit()

    return response.choices[0].message.content, db_entrevista.id


def get_avaliacao(entrevista_id: str, respostas: str, db: Session):
    cria_arquivo_respostas(respostas, entrevista_id)
    db_entrevista = db.query(EntrevistaModel).filter(EntrevistaModel.id == entrevista_id).first()
    db_entrevista.link_audio = f'https://pontochaveai.s3.amazonaws.com/respostas_{entrevista_id}.txt'

    perguntas = get_text_from_s3(db.query(EntrevistaModel.link_perguntas).filter(EntrevistaModel.id == entrevista_id).first()[0])
    response = client.chat.completions.create(
    model="gpt-4o",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "Você é um entrevistador rígido entrevistando um candidato a emprego com saída no formato JSON. Utilize o pronome 'Você' para se referir ao candidato."},
        {"role": "user", "content": "Considerando as perguntas:["+perguntas+"] e somente as respostas:["+respostas+"], forneça um feedback com a saída no seguinte formato: {'pontos_fortes': {'resposta(numero)': (feedback), 'resposta(numero)': (feedback)}, 'pontos_fracos': {'resposta(numero)': (feedback), 'resposta(numero)': (feedback)} }. Siga essa estrutura de JSON para cada uma das respostas das perguntas (considere também deixar o valor para as chaves dos pontos fortes e fracos em branco caso não seja conveniente colocar algo, mas mantenha todas as chaves no formato resposta(numero)). Coloque nos pontos fracos o que o candidato pode melhorar e o motivo."}
    ],
    max_tokens=1000,
    temperature=0.9
    )
    cria_arquivo_avaliacao(response.choices[0].message.content, entrevista_id)
    db_entrevista.link_avaliacao = f'https://pontochaveai.s3.amazonaws.com/avaliacao_{entrevista_id}.txt'
    db.commit()
    return response.choices[0].message.content