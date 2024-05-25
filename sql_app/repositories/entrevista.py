from Singleton import SingletonMeta
from database import get_db
from sqlalchemy.orm import Session
from models.entrevista import EntrevistaModel
#import httpexception
from fastapi import HTTPException

class EntrevistaRepository(metaclass= SingletonMeta):

    def create_entrevista(self,entrevista_db: EntrevistaModel,db: Session):
        try:
            db.add(entrevista_db)
            db.commit()
            db.refresh(entrevista_db)
        except:
            db.rollback()
            raise HTTPException(status_code=500,detail='Não foi possível salvar no banco de dados')
        finally:
            db.close()
        return entrevista_db
    
    
    def get_entrevista(self,db: Session, id: int):
        return db.query(EntrevistaModel).filter(EntrevistaModel.id == id).first()

    
    def get_pergunta_from_entrevista(self,db:Session,entrevista_id:int):
        return db.query(EntrevistaModel.link_perguntas).filter(EntrevistaModel.id == entrevista_id).first()[0]
    
    def only_database_commit(self,db:Session):
        try:
            db.commit()
        except:
            raise HTTPException(status_code=500,detail='Erro ao salvar')
        return 