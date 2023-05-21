# About

The backend uses, among others, the following technologies:
- FastAPI: a fast Python framework for API development with great support to async IO operations, like HTTP requests and database communication. It also counts with built-in OpenAPI schema generation;
- Postgres: due to previous experiences, its popularity, and useful features like JSON fields and [full-text-search](https://github.com/rafael-frs-a/django_memes#dependencies).
- SQLModel: for database ORM;
- Alembic: for managing database migrations;
- [pip-tools](https://github.com/jazzband/pip-tools): to handle dependency files. Although as not convenient as `poetry`, it doesn't make it necessary to be added to the Docker image, since the `requirements.txt` file it generates can be installed with just `pip`;
- Flake8: to lint files;
- Bandit: to check the code for potential security vulnerabilities;
- Mypy: to enforce type checking on all Python files;
- Pytest + pytest-cov: to run all unit tests. Coverage is set to 100% (with omissions).

The `/bin` folder contains bash files meant to be used with CI/CD pipelines. It consists of:
- `check_linting.sh`: runs flake8;
- `check_security.sh`: runs bandit;
- `check_types.sh`: runs mypy;
- `create_db.sh`: creates the database if it doesn't exist using a set up CLI command;
- `migrate.sh`: runs migrations against configured and existing database;
- `run_tests.sh`: runs pytest tests;
- `start.sh`: starts API server.
