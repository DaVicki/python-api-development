from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import String

# Base Post schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# PostCreate 
class PostCreate(PostBase):
    pass

# Reponse
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True