# import openai
import openai
from openai import OpenAI
client = OpenAI()
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# def get_perguntas(vaga, curriculo):
#     return "Perguntas"

# def get_avaliacao(perguntas, respostas):
#     return "Avaliacao"

def get_perguntas(vaga, curriculo):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "Você é um entrevistador conversando com um candidato a emprego com saída no formato JSON."},
        {"role": "user", "content": f"Me de perguntas personalizadas para a vaga: {vaga}, com esse curriculo: {curriculo}"}
    ],
    max_tokens=100,
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

