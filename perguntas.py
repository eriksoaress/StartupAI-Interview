# import openai
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = "sk-proj-WxAsw3rOgrruaV4B0MVDT3BlbkFJvvTv4tscyMEMKw6vfVii"


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, "r") as arquivo:
        return arquivo.read()


def perguntas(vaga, curriculo):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=(f"Com base na descricao da vaga: {vaga} e no curriculo: {curriculo}, escreva uma pergunta que poderia ser feita para o candidato:"),
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.9
    )
    return response.choices[0].text.strip()

texto = ler_arquivo("arquivo.txt")
pergunta = perguntas(texto)
print(pergunta)


# def avaliacao(perguntas, respostas):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=(f"Com base nas perguntas: {perguntas} e nas respostas: {respostas}, escreva uma avaliacao sobre as respostas:"),
#         max_tokens=1000,
#         n=1,
#         stop=None,
#         temperature=0.9
#     )
#     return response.choices[0].text.strip()

# resposta = ler_arquivo("respostas.txt")
# avaliacao = avaliacao(pergunta, resposta)
# print(avaliacao)
