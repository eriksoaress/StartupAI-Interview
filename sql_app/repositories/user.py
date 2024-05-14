from Singleton import SingletonMeta
from database import get_db
from sqlalchemy.orm import Session
from models.user import UserModel

class UserRepository(metaclass= SingletonMeta):

    def signup(self,user_db: UserModel,db: Session):
        try:
            db.add(user_db)
            db.commit()
            db.refresh(user_db)
        except:
            db.rollback()
            raise
        finally:
            db.close()
        print("User added")
        return user_db
    
    def get_user(self,db: Session, email: str):
        return db.query(UserModel).filter(UserModel.email == email).first()