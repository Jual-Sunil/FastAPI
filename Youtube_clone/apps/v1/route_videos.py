from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

router = APIRouter()

@router.get('/homepage')
def homepage(request : Request):
    return templates.TemplateResponse('video_pages/homepage.html', {'request': request})