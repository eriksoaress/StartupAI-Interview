from fastapi import FastAPI
from sql_app.controller.entrevista_controller import *
from sql_app import models
from .database import engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(entrevista_router)