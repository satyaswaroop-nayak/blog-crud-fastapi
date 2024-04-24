from pydantic import BaseModel
from typing import List

# Blog:
    # id:
    # title:
    # body:
    # user_id:

# User:
#     id:
#     name:
#     email_id:
#     blogs:

class BlogBase(BaseModel):
    title: str
    body: str

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email_id: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    blogs: List[Blog] = []
    class Config:
        orm_mode = True
