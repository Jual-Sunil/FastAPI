from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username : str = Field(min_length=4)
    email : EmailStr
    password : str = Field(..., min_length=4)

class ShowUser(BaseModel):
    id : int
    email : EmailStr
    username : str
    is_active : bool

    class Config():
        orm_mode = True