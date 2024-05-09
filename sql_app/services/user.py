from Singleton import SingletonMeta
from repositories.user import UserRepository
from sqlalchemy.orm import Session
from models.user import UserModelTest
from schemas.user import UserTest

class UserService(metaclass=SingletonMeta):
    def __init__(self):
        # self.db = db
        self.user_repo = UserRepository()

    def signup(self,user: UserTest):
        user_ = UserModelTest(name=user.name)
        return self.user_repo.signup(user_)

