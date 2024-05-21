from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from Singleton import SingletonMeta
from repositories.user import UserRepository
from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user import UserTest
from schemas.roles import Roles
from passlib.context import CryptContext
import os
from schemas.user import UserIn
from schemas.token import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_HASH_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

class UserService(metaclass=SingletonMeta):
    def __init__(self):
        # self.db = db
        self.user_repo = UserRepository()

    def signup(self,user: UserIn,db: Session):
        try:
            user_ = UserModel(name=user.name,email=user.email,password=get_password_hash(user.password),is_active=True,role=Roles.free)
            return self.user_repo.signup(user_,db)
        except Exception as e:
            if "Duplicate entry" in str(e):
                raise HTTPException(status_code=400, detail="Email já está registrado!")
            raise HTTPException(status_code=400, detail="Erro criando usuário! Verifique os dados informados!")

        

    def authenticate_user(self,db, email: str, password: str):
        user = self.user_repo.get_user(db, email)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def get_current_user(self,db,token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        user = self.user_repo.get_user(db, email=token_data.email)
        if user is None:
            raise credentials_exception
        return user
    
    def get_current_active_user(
        current_user: Annotated[UserModel, Depends(get_current_user)],
    ):
        if ~current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    




