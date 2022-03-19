from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Post(BaseModel): # This BaseModel defines how request/response should look
                       # It's used for validation purposes, it gives constraints to user  
                       # This means that user can't provide us any schema he wants 
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass    


class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:           # need this subclass to convert sqlalchemy model to pydantic model 
                            # in order to FastAPI return values correctly
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None   