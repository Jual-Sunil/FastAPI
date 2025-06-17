from fastapi import APIRouter,Depends,Request, responses, Form, status, Cookie
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.core.config import settings
from fastapi import responses, HTTPException
import random,string

from google.oauth2 import id_token as google_token
from google.auth.transport import requests as google_requests

from backend.db.session import get_db
from backend.db.repo.user import create_new_user
from backend.db.repo.login import get_user_by_email
from backend.schemas.user import UserCreate
from backend.core.security import create_access_token
from backend.apis.v1.route_login import auth_user
from backend.apis.v1.route_login import token_from_cookie
from authlib.integrations.starlette_client import OAuth

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter()
oauth = OAuth()

oauth.register(
    name= 'google',
    client_id = settings.GOOGLE_CLIENT_ID,
    client_secret = settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs = {'scope' : 'openid email profile',
                     'prompt' : 'consent',
                     'redirect_url': 'http://localhost:8000/login' }
    )

def rand_passgen(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=length))
    return password



@router.get("/login")
def login_page(request : Request):
    error = request.session.pop("error", [])
    return templates.TemplateResponse("auth/login.html", {"request":request, 'error' : error})

@router.post("/login")
def login_form(
    request : Request,
    email : str = Form(...),
    password : str = Form(...),
    db : Session = Depends(get_db)
    ):
    error = []
    Logs = {"request" : request,"error" : error,"email" : email, "password" : password}
    user = auth_user(email=email, password=password, db=db)
    if not user:
        error.append("Incorrect email or password")
        return templates.TemplateResponse("auth/login.html",Logs)
    access_token = create_access_token(data = {"sub" : email})
    response = responses.RedirectResponse(url='/?alert=Successfully logged in!', status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}")
    return response

@router.get("/login/google")
async def google_login(request : Request):
    url = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, url)

@router.get("/google/callback", name='auth_google_callback')
async def google_callback(request : Request, db : Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    id_token_str = token.get("id_token")
    if not id_token_str:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID token not found.")
    try:
        user_info = google_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid ID token: {str(e)}")
    name = user_info.get("name")
    email = user_info.get("email")
    prof_img = user_info.get("picture")
    print(f"Username:{name} \n Email: {email} \n Image: {prof_img}")
    user = get_user_by_email(email= email,db=db)
    if not user:
        user_data = UserCreate(username = name, email=email, password = rand_passgen(), prof_img = prof_img)
        create_new_user(user=user_data, db=db)
    
    access_token = create_access_token(data={"sub" : email})
    response = responses.RedirectResponse(url="/?alert=Successfully logged in with google!", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}")
    return response

@router.get("/logout")
def logout():
    response = responses.RedirectResponse('/', status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response