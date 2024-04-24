from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status
from passlib.context import CryptContext

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

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_blog(db: Session, blog: schemas.BlogCreate, user_id: int):
    db_blog = models.Blog(**blog.model_dump(), user_id=user_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def retrieve_blogs(db: Session, user_id: int):
    return db.query(models.Blog).filter(models.Blog.user_id==user_id).all()

def retrieve_blog_by_id(db: Session, blog_id: int):
    blog = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {blog_id} not found")
    return blog

def update_blog(db: Session, blog_id: int, request: schemas.BlogCreate):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {blog_id} not found")

    blog.update(dict(request))
    db.commit()
    return {'response':'updated'}

def delete_blog(db: Session, blog_id: int):
    blog = db.query(models.Blog).filter(models.Blog.id==blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"response":"deleted"}

def create_user(db: Session, user: schemas.UserCreate):
    hashedPassword = pwd_cxt.hash(user.password)
    new_user = models.User(name = user.name, email_id = user.email_id, password
                            = hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def retrieve_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    return user

def update_user():
    pass

def delete_user():
    pass