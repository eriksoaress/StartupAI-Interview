from fastapi import APIRouter,File, UploadFile, Depends,Form, HTTPException
from services.entrevista_service import *
from sqlalchemy.orm import Session
from typing import Optional
from schemas.perguntasInDTO import PerguntasInDTO
from database import get_db
from services.user import *
from services.entrevista_service import *

entrevista_router = APIRouter( prefix="/entrevistas", tags=["entrevistas"])


service = UserService()
entrevista_service = EntrevistaService()

@entrevista_router.post("/perguntas")
async def read_perguntas(vaga : str = Form(...),
                        link_descricao: str = Form(...),
                        file: UploadFile = File(...),
                        user_id: int = Form(...),
                        db: Session = Depends(get_db),
                        token: str = Depends(oauth2_scheme)):
    if not file.filename.endswith('.pdf') and not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Formato de arquivo inválido")
    contents = await file.read()
    entrevista = PerguntasInDTO(vaga=vaga, link_descricao=link_descricao, user_id=user_id)
    return entrevista_service.get_perguntas(entrevista, contents, file.filename ,db)


@entrevista_router.post("/respostas")
def read_avaliacao(entrevista_id: str = Form(...),
                   link_audio: str = Form(...),
                    db: Session = Depends(get_db),
                    token: str = Depends(oauth2_scheme)):
    return entrevista_service.get_avaliacao(entrevista_id, link_audio, db)

@entrevista_router.post("/audio")
async def read_audio(file: UploadFile = File(...), db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    transcription = await transc_audio(file, db)
    return transcription
