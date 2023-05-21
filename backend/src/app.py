from fastapi import FastAPI
from src import api
from src.api import config

app = FastAPI(title=config.APP_NAME)
api.init_app(app)
