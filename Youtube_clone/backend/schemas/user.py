from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    username : str = Field(min_length=4)
    email : EmailStr
    password : str = Field(..., min_length=4)
    prof_img : Optional[str] = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"


class ShowUser(BaseModel):
    id : int
    email : EmailStr
    username : str
    prof_img : str
    is_active : bool

    class Config():
        orm_mode = True