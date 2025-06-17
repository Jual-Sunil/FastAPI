from datetime import datetime, timedelta
from typing import Optional
from jose import jwt 
from backend.core.config import settings

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    print(f"Added time to token for expiry: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, settings.KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt