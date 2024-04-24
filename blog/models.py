from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

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

class Blog(Base):
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates='blogs')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email_id = Column(String)
    password = Column(String)

    blogs = relationship('Blog', back_populates='user')