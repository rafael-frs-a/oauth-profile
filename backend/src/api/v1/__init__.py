from fastapi import FastAPI
from src.api import config
from .auth import views as auth_views
from .user import views as user_views

v1 = FastAPI(title=config.APP_NAME, version='1.0')
v1.include_router(auth_views.router)
v1.include_router(user_views.router)
