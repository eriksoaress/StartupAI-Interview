# import openai
import openai
from openai import OpenAI
client = OpenAI()
from dotenv import load_dotenv
import os
import io
from PyPDF2 import PdfReader

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_perguntas(vaga, contents):
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
        {"role": "user", "content": f"Me de perguntas personalizadas para a vaga: {vaga}, com esse curriculo: {curriculo}"}
    ],
    max_tokens=1000,
    temperature=0.9
    )
    return response.choices[0].message.content


def get_avaliacao(perguntas, respostas):
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

