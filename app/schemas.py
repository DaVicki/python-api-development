from pydantic import BaseModel
from datetime import datetime

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