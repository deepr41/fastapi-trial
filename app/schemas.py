from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from pydantic.networks import EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password:str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id:Optional[str] = None

class PostBase(BaseModel):
    title : str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    # title : str  #from parent class
    # content: str
    # published: bool
    id:int
    created_at: datetime
    # owner_id:int
    owner:UserOut

    class Config:
        orm_mode = True
    
