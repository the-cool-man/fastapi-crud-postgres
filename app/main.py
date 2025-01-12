import time
from fastapi import Depends, FastAPI, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


    

#Connect to your postgres DB
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connection to database was failed!")
        print(error)
        time.sleep(4)




@app.get("/")
def root():
    return {"Welcome"}



@app.get("/post")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM post ORDER BY id ASC")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {'data': posts}



@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    # cursor.execute("insert into post (title, content, published) values (%s, %s, %s) returning *", (post.title, post.content, post.published) )
    # conn.commit()
    # newPost = cursor.fetchone()
    newPost = models.Post(**post.model_dump())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return {'data': newPost}



@app.get("/post/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM post where id = %s", (str(id)) )
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} is available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { 'message': 'No post available'}
    return {'data': post}


@app.delete("/post/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("delete FROM post where id = %s returning *", (str(id),) )
    # deletedPost = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} is available to delete")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return {'data': 'deleted Post'}


@app.put("/post/{id}")
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db)):
    # cursor.execute("update post set title= %s, content = %s, published = %s where id = %s returning * ", 
    #                 (post.title, post.content, post.published, str(id))
    #               )
    
    # updatedPost = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = post_query.first()
    
    if post_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} is available to update")

    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    
    return {'data': post_query.first()}
