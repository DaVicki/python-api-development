from sqlalchemy import create_engine, text
from faker import Faker
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

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

faker = Faker('en_US')

for i in range(10):
    LOGGER.info(f'Inserting record number {i + 1}')
    id = faker.random_int(min=1, max=200)
    title = faker.name()
    content = faker.text()

    insert_query = text("INSERT INTO davicki.posts (id, title, content) VALUES (:id, :title, :content)")

    try:
        with engine.connect() as connection:
            # Use a transaction block to ensure changes are committed
            with connection.begin():
                connection.execute(insert_query, {"id": id, "title": title, "content": content})
            LOGGER.info(f"Data inserted successfully {i + 1}")
    except Exception as error:
        LOGGER.warning(f"Failed to insert record {i + 1}: {error}")

engine.dispose()