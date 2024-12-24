from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from faker import Faker
import logging
import models, utils
from config import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@postgres:5432/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_SCHEMA_NAME = 'davicki'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_schema():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.execute(CreateSchema(SQLALCHEMY_SCHEMA_NAME, if_not_exists=True))
        session.commit()
        LOGGER.info("Schema created successfully.")
    except Exception as e:
        LOGGER.info(f"Error creating schema: {e}")
    finally:
        session.close()

def seed():
    faker = Faker('en_US')

    # check if database has some seed data
    if next(get_db()).query(models.User).first() is not None:
        LOGGER.info('Database already seeded')
        return
    
    # set up a default user
    default_user = 'admin@admin.com'
    default_password = 'admin'

    sample_user = {'email': default_user, 'password': utils.hash_password(default_password)}
    model_user = models.User(**sample_user)
    insert_record(model_user)

    # seed some fake posts
    for i in range(10):
        sample_post = {'title': faker.name(), 'content': faker.text(), 'owner_id': model_user.id, 'published': faker.boolean()}
        model_post = models.Post(**sample_post)
        insert_record(model_post) 

        sample_vote = {'post_id': model_post.id, 'user_id': model_user.id}
        model_vote = models.Vote(**sample_vote)
        insert_record(model_vote) 

def insert_record(model): 
    db_generator = get_db()
    db = next(db_generator)


    try:
        db.add(model)
        db.commit()
        db.refresh(model)
    finally:
        db_generator.close()
    
    # log the model dump
    LOGGER.info(f'Inserted record {model}')
    if hasattr(model, 'id'):
        return model.id
