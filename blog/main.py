from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, crud
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
# from passlib.context import CryptContext
from typing import List

app = FastAPI()
models.Base.metadata.create_all(engine)

# pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog/{user_id}', status_code=status.HTTP_201_CREATED, tags=['blogs'], response_model=schemas.Blog
          )
def createBlog(blog: schemas.BlogCreate, user_id: int, db: Session=Depends(get_db)):
    return crud.create_blog(db, blog, user_id)

@app.get('/blog/read-all/{user_id}', tags=['blogs'], response_model=List[schemas.Blog])
def getBlogs(user_id: int, db:Session = Depends(get_db)):
    return crud.retrieve_blogs(db, user_id)

@app.get('/blog/read/{blog_id}', status_code=200, response_model=schemas.Blog, tags=['blogs'])
def getBlog(blog_id: int,db: Session = Depends(get_db)):
    return crud.retrieve_blog_by_id(db, blog_id)

@app.put('/blog/update/{blog_id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def updateBlog(blog_id: int, request: schemas.BlogCreate, db:Session=Depends(get_db)):
    return crud.update_blog(db, blog_id, request)

@app.delete('/blog/delete/{blog_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def deleteBlog(blog_id: int, db:Session=Depends(get_db)):
    return crud.delete_blog(db, blog_id)


@app.post('/user', response_model=schemas.User, tags=['user'])
def createUser(request: schemas.UserCreate, db:Session=Depends(get_db)):
    return crud.create_user(db, request)

@app.get('/user/read/{user_id}', response_model=schemas.User, tags=['user'])
def getUser(user_id:int, db:Session=Depends(get_db)):
    return crud.retrieve_user(db, user_id)