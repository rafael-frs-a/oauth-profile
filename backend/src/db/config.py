import os
from src import utils

utils.load_env()

DB_USERNAME = os.getenv('DB_USERNAME', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '')
DB_PORT = os.getenv('DB_PORT', '')
DB_NAME = os.getenv('DB_NAME', '')
DB_ENCRYPTION_KEY = os.getenv('DB_ENCRYPTION_KEY', '')
