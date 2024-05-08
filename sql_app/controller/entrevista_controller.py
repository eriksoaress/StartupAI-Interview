from fastapi import APIRouter,File, UploadFile, Depends,Form
from PyPDF2 import PdfReader
import io
from service.entrevista_service import *
import io
from schemas_ import Entrevista, EntrevistaBase
from sqlalchemy.orm import Session
from typing import Annotated
from typing import Optional
from schemas.perguntasInDTO import PerguntasInDTO
from database import get_db



entrevista_router = APIRouter( prefix="/entrevistas", tags=["entrevistas"])

@entrevista_router.post("/perguntas")
async def read_perguntas(vaga : str = Form(...),
                        descricao: Optional[str] = Form(None),
                        file: UploadFile = File(...),
                        db: Session = Depends(get_db)):
    
    if not file.filename.endswith('.pdf'):
        return {"error": "Por favor, anexe um arquivo PDF"}
    contents = await file.read()
    entrevista = PerguntasInDTO(vaga=vaga, descricao=descricao)
    return get_perguntas(entrevista, contents, db)


@entrevista_router.post("/respostas")
def read_avaliacao(entrevista_id: str,
                   link_audio: str,
                    db: Session = Depends(get_db)):
    return get_avaliacao(entrevista_id, link_audio, db)
