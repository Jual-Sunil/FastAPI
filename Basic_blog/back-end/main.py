from fastapi import FastAPI
from core.config import Settings

def start_app():
    app = FastAPI(title=Settings.PROJECT_TITLE, version=Settings.PROJECT_VERSION)
    return app

app =  start_app()

@app.get('/')
def hello():
    return 'Hello world'