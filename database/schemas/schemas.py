from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    image_url:str
    title:str
    content:str
    creator:str
    owner_id: int
   
class PostDisplay(PostBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    role: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None 

class User(UserBase):
    id: int
    posts: List[PostDisplay] = []
    class Config:
        orm_mode = True

class LoginCredentials(BaseModel):
    email: str
    password: str

