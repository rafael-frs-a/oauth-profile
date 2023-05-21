from src.db import utils

# Call it like `python -m src.cli.create_db`
if __name__ == '__main__':
    utils.create_db_if_not_exists()
    print('Database created successfully')
