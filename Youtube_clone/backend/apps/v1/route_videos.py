from fastapi import APIRouter, Request, status
from fastapi import Depends, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import random

from backend.db.session import get_db
from backend.apis.v1.route_login import get_curr_user
from backend.db.models.users import User
from backend.db.models.videos import Video

templates = Jinja2Templates(directory='frontend/templates')

router = APIRouter()

def format_duration(seconds):
    seconds = int(seconds or 0)
    hours = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return (f"{hours}:{mins:02}:{secs:02}")
    else:
        return (f"{mins:02}:{secs:02}")

templates.env.filters['format_duration'] = format_duration

@router.get('/')
def homepage(
    request : Request, 
    user : User = Depends(get_curr_user), 
    db : Session = Depends(get_db)
):
    if isinstance(user, RedirectResponse):
        return user
    all_vids = db.query(Video).filter(Video.is_active == True).all()
    random.shuffle(all_vids)
    context = {
        'request': request, 
        "username" : None,
        'prof_img' : None, 
        'videos' : all_vids
    }
    if user:
        context['username'] = user.username
        context['prof_img'] = user.prof_img
    else:
        context['Welcome_message'] = 'Please login to begin browsing videos'
    return templates.TemplateResponse('video_pages/homepage.html', context )

@router.get('/videos/{video_id}')
def video_load(
    video_id : str,
    request : Request,
    user : User = Depends(get_curr_user),
    db : Session = Depends(get_db)
):
    video = db.query(Video).filter(Video.id == video_id, Video.is_active == True).first()
    if not video:
        return templates.TemplateResponse('404.html', {'request' : request}, status_code=status.HTTP_404_NOT_FOUND)
    recommendations = db.query(Video).filter(
        Video.id != video_id,
        Video.is_active == True
    ).all()

    random.shuffle(recommendations)
    recommendations = recommendations[:30]
    context = {'request' : request, 'video' : video ,'recommendations' : recommendations, "username" : user.username,'prof_img' : user.prof_img}
    return templates.TemplateResponse('video_pages/video_play.html',context)

@router.get('/search')
def search (
    request : Request, 
    db : Session = Depends(get_db), 
    user : User = Depends(get_curr_user),
    query : str = Query(..., min_length=1)
):
    #Simple search based on word entered
    videos = db.query(Video).filter(
        Video.is_active == True,
        (Video.title.ilike(f'%{query}%') | (Video.desc.ilike(f'%{query}%')))
    ).all()

    context = {'request' : request, 'videos' : videos, 'query' : query, "username" : user.username,'prof_img' : user.prof_img}
    return templates.TemplateResponse('video_pages/searchpage.html', context)