from fastapi import FastAPI 
import logging
from routers import user, post, auth, vote
from alembic.config import Config
from alembic import command
import database_migration
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Run Alembic migrations during application startup
    database_migration.run_migrations()

    # seed data
    database_migration.seed()

# CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

