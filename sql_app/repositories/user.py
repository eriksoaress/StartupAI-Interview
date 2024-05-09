from Singleton import SingletonMeta
from database import get_db

class UserRepository(metaclass= SingletonMeta):

    def signup(self,user_db):
        with get_db() as db:
            try:
                db.add(user_db)
                db.commit()
                db.refresh(user_db)
            except:
                db.rollback()
                raise
        print("User added")
        return user_db