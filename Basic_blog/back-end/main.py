from fastapi import FastAPI
from core.config import Settings
from apis.base import api_router

def include_router(app):
    app.include_router(api_router)

def start_app():
    app = FastAPI(title=Settings.PROJECT_TITLE, version=Settings.PROJECT_VERSION)
    include_router(app)
    return app

app =  start_app()



@app.get('/')
def hello():
    return 'Hello world'

