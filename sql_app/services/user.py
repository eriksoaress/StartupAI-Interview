from Singleton import SingletonMeta
from repositories.user import UserRepository
from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user import UserTest
from schemas.roles import Roles

class UserService(metaclass=SingletonMeta):
    def __init__(self):
        # self.db = db
        self.user_repo = UserRepository()

    def signup(self,user: UserTest,db: Session):
        user_ = UserModel(name=user.name,email=user.email,password=user.password,is_active=True,role=Roles.free)
        return self.user_repo.signup(user_,db)

