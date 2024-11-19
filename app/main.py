from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, text
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

app = FastAPI()

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2}
    ]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

def get_db_engine():
    return create_engine('postgresql://{}:{}@{}/{}'.format('postgres', 'postgres', 'postgres:5432', 'fastapi'))

while True:
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            print("Connected to the database.")
            break
    except Exception as error:
        LOGGER.warning("Connection to database failed")
        LOGGER.warning("Error:", error)
        time.sleep(1)

# Path Operation

# Decorator - turns function into a path operator
@app.get("/")
def root():
    return {"message": "Hello World! Welcome !!!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    id = len(my_posts) + 1
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts.append(post_dict)
    return find_post(id)
# title, content str

# order matters 
@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[-1]
    return {"latest_post": latest_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post} 

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    
    return {"data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def find_post(id: int):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None

def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None