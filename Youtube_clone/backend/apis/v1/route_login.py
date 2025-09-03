#For secure login functions
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError, ExpiredSignatureError
from backend.core.security import create_access_token
#For Base functions
from fastapi import Depends, APIRouter, status, HTTPException,responses, Cookie, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.db.session import get_db
from backend.db.models.users import User
from backend.core.hashing import Hasher
from backend.db.repo.login import get_user_by_email

router =  APIRouter()

def auth_user(email : str, password : str, db : Session):
    user = get_user_by_email(email = email, db = db)
    print(user)
    if not user :
        return False
    if not Hasher.verify_pass(password,user.password):
        return False
    return user

@router.post("/token")
def login_access_token(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = auth_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            detail="Incorrect email or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    access_token = create_access_token(data={"sub" : user.email})
    return ({"access_token" : access_token, "token_type" : "bearer"})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

def token_from_cookie(access_token : str = Cookie(None)):
    if not access_token:
        return None
    return access_token.replace("Bearer", "").strip()

def get_curr_user( request: Request, token : str = Depends(token_from_cookie), db : Session = Depends(get_db)) -> User:
    error = []
    if not token:
        return None
    try:
        payload = jwt.decode(token,settings.KEY, algorithms=settings.ALGORITHM)
        email : str = payload.get("sub")
        print("Payload :" , payload)
        if email is None:
            raise JWTError("Invalid token payload")
    except JWTError:
        response = responses.RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        response.delete_cookie("access_token")
        print("Invalid token")
        return None
        #return response
    except ExpiredSignatureError:
        response = responses.RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie("access_token")
        print("Token expired")
        return None
        #return response
    user = get_user_by_email(email=email,db=db)
    if user is None:
        return None
    return user