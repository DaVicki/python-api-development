from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import insert, select, delete, update
import logging
import time

import models
import database

from fastapi import Depends

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

models.database.Base.metadata.create_all(bind=database.engine)
database.seed()

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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts")
def get_posts():
    Session = sessionmaker(bind=engine)
    session = Session()

    # Step 3: Reflect the existing database
    metadata = MetaData()
    posts_table = Table("posts", metadata, schema="davicki", autoload_with=engine)

    # Step 4: Execute a SELECT * query
    with engine.connect() as connection:
        result = connection.execute(posts_table.select())
        posts_table_data = [row._mapping for row in result]

    return {"data": posts_table_data}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Step 3: Reflect the existing database
    metadata = MetaData()
    posts_table = Table("posts", metadata, schema="davicki", autoload_with=engine)

    insert_stmt = insert(posts_table).values(title=post.title, content=post.content, published=post.published)
    try:
        with engine.connect() as connection:
            # Use a transaction block to ensure changes are committed
            with connection.begin():
                result = connection.execute(insert_stmt)
                # Get the inserted primary key
                inserted_id = result.inserted_primary_key[0]
            
                # Fetch the inserted record
                fetch_stmt = select(posts_table).where(posts_table.c.id == inserted_id)
                inserted_record = connection.execute(fetch_stmt).mappings().first()

                LOGGER.info(f"Inserted record: {inserted_record}")
            LOGGER.info(f"Data inserted successfully")
    except Exception as error:
        LOGGER.warning(f"Failed to insert record: {error}")
        
    return {"data": inserted_record}
# title, content str

# order matters 
@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[-1]
    return {"latest_post": latest_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Step 3: Reflect the existing database
    metadata = MetaData()
    posts_table = Table("posts", metadata, schema="davicki", autoload_with=engine)

    try:
        with engine.connect() as connection:
            # Use a transaction block to ensure changes are committed
            with connection.begin():
                # Fetch the inserted record
                fetch_stmt = select(posts_table).where(posts_table.c.id == id)
                post_by_id = connection.execute(fetch_stmt).mappings().first()
    except Exception as error:
        LOGGER.warning(f"cannot find post by id: {error}")
    
    if not post_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        
    return {"data": post_by_id}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Step 3: Reflect the existing database
    metadata = MetaData()
    posts_table = Table("posts", metadata, schema="davicki", autoload_with=engine)

    update_stmt = (
            update(posts_table)
            .where(posts_table.c.id == id)
            .values(
                {col: val for col, val in {"title": post.title, "content": post.content, "published": post.published}.items() if val is not None}
            )
        )
    try:
        with engine.connect() as connection:
            # Use a transaction block to ensure changes are committed
            with connection.begin():
                result = connection.execute(update_stmt)
                fetch_stmt = select(posts_table).where(posts_table.c.id == id)
                updated_post = connection.execute(fetch_stmt).mappings().first()

                if result.rowcount > 0:
                    LOGGER.info(f"Updated record with id = {id}")
                else:
                    LOGGER.warning(f"No record found with id = {id}")

    except Exception as error:
        LOGGER.warning(f"Failed to update record: {error}")

    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return {"data": updated_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Step 3: Reflect the existing database
    metadata = MetaData()
    posts_table = Table("posts", metadata, schema="davicki", autoload_with=engine)

    try:
        with engine.connect() as connection:
            # Use a transaction block to ensure changes are committed
            with connection.begin():
                # Fetch the inserted record
                delete_stmt = delete(posts_table).where(posts_table.c.id == id)
                result = connection.execute(delete_stmt)
                if result.rowcount > 0:
                    LOGGER.info(f"Deleted record with id = {id}")
                else:
                    LOGGER.warning(f"No record found with id = {id}")
    except Exception as error:
        LOGGER.warning(f"cannot delete post by id: {error}")
    
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        
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
