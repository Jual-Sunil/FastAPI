from fastapi import APIRouter, Request
from fastapi import Depends
from typing import Optional
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.repository.blog import list_blogs,retrieve_blog
from db.session import get_db

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/")
def home (request : Request, alert : Optional[str] = None , db : Session = Depends(get_db)):
    blogs = list_blogs(db = db)
    if not blogs:
        return "Blog is empty"
    context = {"request" : request, "blogs" : blogs, "alert" : alert}
    return templates.TemplateResponse("blogs/home.html", context=context)

@router.get("/app/blog/{id}/")
def blog_desc(request : Request, id : int, db : Session = Depends(get_db)):
    blog = retrieve_blog(id = id, db = db)
    context = {"request" : request, "blog" : blog}
    return templates.TemplateResponse("blogs/desc.html", context=context)
