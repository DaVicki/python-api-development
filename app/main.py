from fastapi import FastAPI 
import logging, models, database, config
from routers import user, post, auth

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

# set up database
database.create_schema()
# create tables
models.database.Base.metadata.create_all(bind=database.engine)
# seed data
database.seed()

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

