from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
import logging
from config import settings

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

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
        LOGGER.info(f"Creating schema...{settings.database_schema}")
        session.execute(CreateSchema(
            settings.database_schema, if_not_exists=True))
        session.commit()
        LOGGER.info("Schema created successfully.")
    except Exception as e:
        LOGGER.info(f"Error creating schema: {e}")
    finally:
        session.close()