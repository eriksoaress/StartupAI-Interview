from fastapi import FastAPI
from controller.entrevista_controller import *
import models
from database import engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(entrevista_router)
