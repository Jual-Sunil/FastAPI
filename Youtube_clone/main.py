from fastapi import FastAPI
from core.config import Settings
from apis.base import api_router
from apps.base import app_router
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

settings = Settings()

#func for adding routers
def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)
#func for adding static files
#def configure_staticfiles(app):
    #app.mount("/static",StaticFiles(directory="static"),name="static")

def start_app():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    app.add_middleware(SessionMiddleware, secret_key=settings.KEY)
    include_router(app)
    #configure_staticfiles(app)
    return app

app = start_app()