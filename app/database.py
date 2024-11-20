from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from faker import Faker
import logging

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

def seed():
    faker = Faker('en_US')

    for i in range(10):
        LOGGER.info(f'Inserting record number {i + 1}')
        title = faker.name()
        content = faker.text()
        published = faker.boolean()

        insert_query = text("INSERT INTO davicki.posts (title, content, published) VALUES (:title, :content, :published)")

        try:
            with engine.connect() as connection:
                # Use a transaction block to ensure changes are committed
                with connection.begin():
                    connection.execute(insert_query, {"title": title, "content": content, "published": published})
                LOGGER.info(f"Data inserted successfully {i + 1}")
        except Exception as error:
            LOGGER.warning(f"Failed to insert record {i + 1}: {error}")

Session = sessionmaker(bind=engine)
session = Session()

try:
    session.execute(CreateSchema(SQLALCHEMY_SCHEMA_NAME, if_not_exists=True))
    session.commit()
    print("Schema created successfully.")
except Exception as e:
    print(f"Error creating schema: {e}")
finally:
    session.close()
    
