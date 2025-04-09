import json
from pydantic import constr
from fastapi import APIRouter,Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi import responses, status, Form
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.user import UserCreate
from db.repository.user import create_new_user
from pydantic.error_wrappers import ValidationError
from apis.v1.route_login import authenticate_user
from core.security import create_access_token

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/register")
def register(request : Request):
    return templates.TemplateResponse("auth/register.html", {"request" : request})

@router.post("/register")
def register(request : Request, email : str = Form(...), password : str = Form(...), db : Session = Depends(get_db)):
    error = []
    try:
        user = UserCreate(email = email, password = password)
        print("User created")
        create_new_user(user=user,db=db)
        print("Returning response")
        return responses.RedirectResponse("/?alert=Successfully%20Registered", status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        error_list = json.loads(e.json())
        for item in error_list:
            error.append(item.get("loc")[0] + ": " + item.get("msg"))
            print(error)
        return templates.TemplateResponse("auth/register.html", {"request": request, "error": error})

@router.get("/login")
def login(request : Request):
    return templates.TemplateResponse("auth/login.html", {"request":request})

@router.post("/login")
def login(request : Request,
          email : str = Form(...),
          password : str = Form(...),
          db : Session = Depends(get_db)):
    error= []
    user = authenticate_user(email=email, password=password, db=db)
    if not user:
        error.append("Incorrect email or password")
        return templates.TemplateResponse("auth/login.html", {"request" : request, "error" : error, "email" : email, "password" : password})
    access_token = create_access_token(data={"sub" : email})
    response = responses.RedirectResponse("/?alert=Successfully logged in", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}")
    return response