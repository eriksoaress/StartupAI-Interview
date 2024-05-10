from Singleton import SingletonMeta
from database import get_db
from sqlalchemy.orm import Session
from models.user import UserModelTest

class UserRepository(metaclass= SingletonMeta):

    def signup(self,user_db: UserModelTest,db: Session):
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