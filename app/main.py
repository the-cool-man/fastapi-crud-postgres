import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel  # Used for validation
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

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





class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: Optional[bool] = False
    # rating: Optional[float] = None


my_post = [
    {'id': 1, 'title': 'Hobby', 'Content': "PS5 Games, Cricket watching"},
    {'id': 2, 'title': 'Language', 'Content': "Python and Javascript"},
    {'id': 3, 'title': 'Food', 'Content': "Dal Fry and Roti"},
]


def findPostByID(id):
    for p in my_post:
        if p['id'] == id:
            return p


def findIndex(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"Welcome"}


@app.get("/post")
def get_posts():
    cursor.execute("SELECT * FROM post ORDER BY id ASC")
    posts = cursor.fetchall()
    return {'data': posts}


@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("insert into post (title, content, published) values (%s, %s, %s) returning *", (post.title, post.content, post.published) )
    conn.commit()
    newPost = cursor.fetchone()
    return {'data': newPost}


@app.get("/post/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM post where id = %s", (str(id)) )
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} is available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { 'message': 'No post available'}
    return {'data': post}


@app.delete("/post/{id}")
def delete_post(id: int):
    cursor.execute("delete FROM post where id = %s returning *", (str(id),) )
    deletedPost = cursor.fetchone()
    conn.commit()

    if deletedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} is available to delete")

    return {'data': deletedPost}


@app.put("/post/{id}")
def update_post(id: int, post: Post):
    postIndex = findIndex(id)
    if postIndex == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} is available to update")

    post_dic = post.model_dump()
    post_dic['id'] = id
    my_post[postIndex] = post_dic
    return {'data': post_dic}
