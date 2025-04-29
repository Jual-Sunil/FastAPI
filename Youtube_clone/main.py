from fastapi import FastAPI
from core.config import Settings
from db.session import engine
from db.base_class import Base
from fastapi.staticfiles import StaticFiles

#func for adding routers
def include_router(app):
    return
#func for adding static files
def configure_staticfiles(app):
    return
#func for creating tables
def create_tables():
    Base.metadata.create_all(bind = engine)

def start_app():
    app = FastAPI(title=Settings.PROJECT_TITLE, version=Settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    configure_staticfiles(app)
    return app

app = start_app()