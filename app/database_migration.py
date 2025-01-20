import os
from alembic import command
from alembic.config import Config
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from faker import Faker
import logging
import models, utils
from config import settings
import os
import database

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

def run_migrations():
    # Get the path to the alembic.ini file
    alembic_cfg_path = os.path.join(os.path.dirname(__file__), "alembic.ini")

    # Load the Alembic Config
    alembic_cfg = Config(alembic_cfg_path)

    # Run the `upgrade` command to apply all migrations
    command.upgrade(alembic_cfg, "head")

def seed():
    faker = Faker('en_US')

    # check if database has some seed data
    if next(database.get_db()).query(models.User).first() is not None:
        LOGGER.info('Database already seeded')
        return

    # set up a default user
    default_user = 'admin@admin.com'
    default_password = 'admin'

    sample_user = {'email': default_user,
                   'password': utils.hash_password(default_password)}
    model_user = models.User(**sample_user)
    insert_record(model_user)

    # seed some fake posts
    for i in range(10):
        sample_post = {'title': faker.name(), 'content': faker.text(
        ), 'owner_id': model_user.id, 'published': faker.boolean()}
        model_post = models.Post(**sample_post)
        insert_record(model_post)

        sample_vote = {'post_id': model_post.id, 'user_id': model_user.id}
        model_vote = models.Vote(**sample_vote)
        insert_record(model_vote)


def insert_record(model):
    db_generator = database.get_db()
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