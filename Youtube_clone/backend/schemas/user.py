from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username : str = Field(min_length=4)
    email : EmailStr
    password : str = Field(..., min_length=4)
    prof_img : str


class ShowUser(BaseModel):
    id : int
    email : EmailStr
    username : str
    prof_img : str
    is_active : bool

    class Config():
        orm_mode = True