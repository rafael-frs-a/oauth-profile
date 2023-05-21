import os
from src import utils

utils.load_env()

APP_NAME = 'OAuth Profile - API'
SECRET_KEY = os.getenv('SECRET_KEY', '')
JWT_ALGORITHM = 'HS256'
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',')
FRONTEND_URL = os.getenv('FRONTEND_URL', '')
