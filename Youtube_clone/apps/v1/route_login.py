import json
from fastapi import APIRouter,Depends,Request, responses, Form, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.config import settings
from fastapi import responses
import random,string

from db.session import get_db
from db.repo.user import create_new_user
from db.repo.login import get_user_by_email
from schemas.user import UserCreate
from core.security import create_access_token
from apis.v1.route_login import auth_user
from pydantic.error_wrappers import ValidationError
from authlib.integrations.starlette_client import OAuth

templates = Jinja2Templates(directory="templates")
router = APIRouter()
oauth = OAuth()

oauth.register(
    name= 'google',
    client_id = settings.GOOGLE_CLIENT_ID,
    client_secret = settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs = {'scope' : 'openid email profile',
                     'redirect_url': 'http://localhost:8000/login' }
    )

def rand_passgen(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=length))
    return password

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
        return responses.RedirectResponse(url='/?alert=Successfully%20Registered!', status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        error_list = json.loads(e.json())
        for item in error_list:
            error.append(item.get("loc")[0] + ": "+item.get("msg"))
        return templates.TemplateResponse("auth/login.html", {"request" : request, "error" : error})

@router.get("/login")
def login_page(request : Request):
    return templates.TemplateResponse("auth/login.html", {"request":request})

@router.post("/login")
def login_form(
    request : Request,
    email : str = Form(...),
    password : str = Form(...),
    db : Session = Depends(get_db)
    ):
    error = []
    user = auth_user(email=email, password=password, db=db)
    if not user:
        error.append("Incorrect email or password")
        return templates.TemplateResponse("auth/login.html",{"request" : request, "email" : email, "password" : password})
    access_token = create_access_token(data = {"sub" : email})
    response = responses.RedirectResponse(url='/?alert=Successfully logged in!', status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer : {access_token}")
    return response

@router.get("/login/google")
async def google_login(request : Request):
    url = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, url)

@router.get("/passenter")
def passenter_page(request : Request):
    return templates.TemplateResponse("auth/passenter.html", {"request" : request})

@router.get("/google/callback",name='auth_google_callback')
async def google_callback(request : Request, db : Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    email = user.get('email')
    name = user.get('name')
    print ("email:", email, "username: ", name)
    user = get_user_by_email(email= email,db=db)
    if not user:
        user_data = UserCreate(username = name, email=email, password = rand_passgen())
        create_new_user(user=user_data, db=db)
    
    access_token = create_access_token(data={"sub" : email})
    response = responses.RedirectResponse(url="/homepage?alert=Successfully logged in with google!", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer : {access_token}")
    return response

