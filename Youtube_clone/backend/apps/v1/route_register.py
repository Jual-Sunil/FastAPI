import json
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form, Depends, responses, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from backend.schemas.user import UserCreate
from backend.db.session import get_db
from backend.db.repo.user import create_new_user

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter()

@router.get("/register")
def register_page(request : Request):
    return templates.TemplateResponse("auth/register.html", {"request" : request})


@router.post("/register")
def register_form(
    request : Request,
    username : str = Form(...),
    email : str = Form(...),
    password : str = Form(...),
    db : Session = Depends(get_db)
    ):
    error = []
    try:
        user = UserCreate(username=username,email=email,password=password)
        create_new_user(user=user, db=db)
        return responses.RedirectResponse(url='/login?alert=Successfully%20Registered! Please login', status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        error_list = json.loads(e.json())
        for item in error_list:
            error.append(item.get("loc")[0] + ": "+item.get("msg"))
        Logs = {"request" : request, "error" : error, "email" : email, "username" : username, "password" : password}
        return templates.TemplateResponse("auth/register.html", Logs )
    except IntegrityError as i:
        db.rollback()
        error_msg = str(i.orig).lower()
        Logs = {"request" : request, "error" : error, "email" : email, "username" : username, "password" : password}
        if 'username' in error_msg:
            error.append("Username already exists")
        elif 'email' in error_msg:
            error.append("Email already exists")
        return templates.TemplateResponse("auth/register.html", Logs)