#For secure login functions
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from core.security import create_access_token
#For Base functions
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from core.config import settings
from db.session import get_db
from core.hashing import Hasher
from db.repo.login import get_user_by_email

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

def get_curr_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    cred_exception = HTTPException(
        detail="Could not verify credentials, please login again",
        status_code=status.HTTP_401_UNAUTHORIZED
    )
    try:
        payload = jwt.decode(token,settings.KEY, algorithms=settings.ALGORITHM)
        email : str = payload.get("sub")
        if email is None:
            raise cred_exception
    except JWTError:
        raise cred_exception
    user = get_user_by_email(email=email,db=db)
    if user is None:
        raise cred_exception
    return user