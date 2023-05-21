from dotenv import load_dotenv


def load_env() -> bool:
    return load_dotenv('.env')
