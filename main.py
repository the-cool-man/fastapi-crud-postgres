from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel  # Used for validation
from random import randrange

app = FastAPI()


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
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

@app.get("/")
def root():
    return {"Welcome"}


@app.get("/post")
def get_posts():
    return { 'data': my_post}


@app.post("/post")
def create_post(payload: Post):
    post_dic = payload.model_dump()
    post_dic["id"] = randrange(0, 100)
    my_post.append(post_dic)
    return { 'data': post_dic }


@app.get("/post/{id}")
def get_post(id: int):
    return { 'data': findPostByID(id)}
