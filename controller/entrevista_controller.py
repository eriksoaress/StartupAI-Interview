from fastapi import APIRouter
from service.entrevista_service import *
from model.perguntas import *
from model.avaliacao import *


entrevista_router = APIRouter( prefix="/entrevistas", tags=["entrevistas"])

@entrevista_router.post("/perguntas")
def read_perguntas(perguntas: Pergunta):
    return get_perguntas(perguntas.vaga, perguntas.curriculo)

@entrevista_router.post("/respostas")
def read_avaliacao(avaliacao: Avaliacao):
    return get_avaliacao(avaliacao.perguntas, avaliacao.respostas)