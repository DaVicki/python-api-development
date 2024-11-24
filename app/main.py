from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional,List
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import insert, select, delete, update
import logging
import schemas
import models
import database
import utils
from routers import user, post

from fastapi import Depends

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)



# set up database
database.create_schema()
models.database.Base.metadata.create_all(bind=database.engine)
database.seed()

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

