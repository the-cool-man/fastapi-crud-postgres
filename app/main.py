from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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


def findIndex(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"Welcome"}


@app.get("/post")
def get_posts():
    return {'data': my_post}


@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    post_dic = payload.model_dump()
    post_dic["id"] = randrange(0, 100)
    my_post.append(post_dic)
    return {'data': post_dic}


@app.get("/post/{id}")
def get_post(id: int):
    post = findPostByID(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} is available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { 'message': 'No post available'}
    return {'data': post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    postIndex = findIndex(id)
    if postIndex != None:
        my_post.pop(postIndex)
    return {'data': my_post}


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
