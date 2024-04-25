from fastapi import FastAPI
from controller.entrevista_controller import entrevista_router


app = FastAPI()

app.include_router(entrevista_router)