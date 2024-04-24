# import openai
import openai
from openai import OpenAI
client = OpenAI()
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, "r") as arquivo:
        return arquivo.read()


def perguntas(vaga, curriculo):
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


curriculo = ler_arquivo("curriculo.txt")
vaga = ler_arquivo("descricaovaga.txt")
print(perguntas(vaga, curriculo))


def avaliacao(perguntas, respostas):
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

respostas = input("Digite as respostas: ")
avaliacao = avaliacao(perguntas, respostas)
print(avaliacao)
