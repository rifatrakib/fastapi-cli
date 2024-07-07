from fastapi import FastAPI

from server.core.config.services import configure_app

app: FastAPI = configure_app()
