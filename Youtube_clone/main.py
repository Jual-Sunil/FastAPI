from fastapi import FastAPI
from core.config import Settings
from fastapi.staticfiles import StaticFiles

#func for adding routers
def include_router(app):
    return
#func for adding static files
def configure_staticfiles(app):
    return
def start_app(app):
    app = FastAPI(title=Settings.PROJECT_TITLE, version=Settings.PROJECT_VERSION)
    include_router(app)
    configure_staticfiles(app)
    return app

app = start_app()