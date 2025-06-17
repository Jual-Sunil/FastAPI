from fastapi import FastAPI
from backend.core.config import Settings
from backend.apis.base import api_router
from backend.apps.base import app_router
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

settings = Settings()

#func for adding routers
def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)
#func for adding static files
def configure_staticfiles(app):
    app.mount("/static",StaticFiles(directory="frontend/static"),name="static")

def start_app():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    app.add_middleware(SessionMiddleware, secret_key=settings.KEY)
    app.add_middleware(
        CORSMiddleware,
        allow_origins =['*'],
        allow_credentials =True,
        allow_methods =['*'],
        allow_headers =['*'],
    )
    include_router(app)
    configure_staticfiles(app)
    return app

app = start_app()