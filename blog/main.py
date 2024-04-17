from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()
models.Base.metadata.create_all(engine)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def createBlog(blog: schemas.Blog, db: Session=Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', tags=['blogs'])
def getBlogs(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def getBlog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).all()
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    return blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def updateBlog(id: int, request:schemas.Blog, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    blog.update(dict(request))
    db.commit()
    return 'updated'

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def deleteBlog(id, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"response":"deleted"}


@app.post('/user', response_model=schemas.ShowUser, tags=['user'])
def createUser(request: schemas.User, db:Session=Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(name = request.name, email = request.email, password
                            = hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['user'])
def getUser(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    return user