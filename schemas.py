from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class Users(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : int

class Posts(BaseModel):
    title : str
    content : str
    publish : bool = True

class PostResponse(BaseModel):
    title : str
    content : str
    publish : bool = True
    id : int
    owner_id : int
    owner : UserOut
    votes : int
    class Config:
        # from_attributes = True
        orm_mode = True


class Vote(BaseModel):
    post_id : int
    dir: conint(le=1)