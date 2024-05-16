from fastapi import APIRouter,File, UploadFile, Depends,Form
from services.entrevista_service import *
from sqlalchemy.orm import Session
from typing import Optional
from schemas.perguntasInDTO import PerguntasInDTO
from database import get_db
from services.user import *

entrevista_router = APIRouter( prefix="/entrevistas", tags=["entrevistas"])


service = UserService()

@entrevista_router.post("/perguntass")
async def read_perguntas(vaga : str = Form(...),
                        link_descricao: Optional[str] = Form(None),
                        file: UploadFile = File(...),
                        user_id: int = Form(...),
                        db: Session = Depends(get_db),
                        token: str = Depends(oauth2_scheme)):
    user = service.get_current_user(db, token)
    if not file.filename.endswith('.pdf'):
        return {"error": "Por favor, anexe um arquivo PDF"}
    contents = await file.read()
    entrevista = PerguntasInDTO(vaga=vaga, link_descricao=link_descricao, user_id=user_id)
    return get_perguntas(entrevista, contents, db)


@entrevista_router.post("/respostas")
def read_avaliacao(entrevista_id: str = Form(...),
                   link_audio: str = Form(...),
                    db: Session = Depends(get_db)):
    return get_avaliacao(entrevista_id, link_audio, db)
