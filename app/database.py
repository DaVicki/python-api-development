from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from faker import Faker
import logging
import models

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@postgres:5432/fastapi'
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
    if next(get_db()).query(models.Post).first() is not None:
        LOGGER.info('Database already seeded')
        return

    for i in range(10):
        schema_post = {'title': faker.name(), 'content': faker.text(), 'published': faker.boolean()}
        model_post = models.Post(**schema_post)

        db_generator = get_db()
        db = next(db_generator)

        try: 
            db.add(model_post)
            db.commit()
            db.refresh(model_post)
        finally:
            db_generator.close()

        LOGGER.info(f'Inserted record number {model_post.id}')

