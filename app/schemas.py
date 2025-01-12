from pydantic import BaseModel  # Used for validation
from typing import Optional


class PostBase(BaseModel):
    #id: Optional[int] = None
    title: str
    content: str
    published: Optional[bool] = True
    
    
class PostCreate(PostBase):
    pass
    
    
class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    class Config:
        orm_mode = True

    