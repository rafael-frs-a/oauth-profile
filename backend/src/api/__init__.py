from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.error import handlers
from src.api.v1 import v1
from . import config, views


def _add_module(parent: FastAPI, module: FastAPI, prefix: str) -> None:
    parent.mount(prefix, module)
    handlers.init_errors(module)


def _setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )


def init_app(app: FastAPI) -> None:
    _setup_cors(app)
    app.include_router(views.router)
    handlers.init_errors(app)
    _add_module(app, v1, '/api/v1')
