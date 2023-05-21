import os
from src import utils

utils.load_env()

AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID', '')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET', '')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', '')
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN

ACCESS_TOKEN_EXP_SECONDS = 30 * 60  # 30 minutes
REFRESH_TOKEN_EXP_SECONDS = 1 * 60 * 60  # 1 hour
MAX_LENGTH_PROFILE_HISTORY = 10
