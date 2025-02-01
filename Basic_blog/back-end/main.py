from fastapi import FastAPI
from core.config import Settings
from db.session import engine
from db.base_class import Base

def create_tables():
    Base.metadata.create_all(bind = engine)

def start_app():
    app = FastAPI(title=Settings.PROJECT_TITLE, version=Settings.PROJECT_VERSION)
    create_tables()
    return app

app =  start_app()

@app.get('/')
def hello():
    return 'Hello world'