import os
import database
from alembic import command
from alembic.config import Config


def run_migrations():
    # Get the path to the alembic.ini file
    alembic_cfg_path = os.path.join(os.path.dirname(__file__), "alembic.ini")

    # Load the Alembic Config
    alembic_cfg = Config(alembic_cfg_path)

    # Run the `upgrade` command to apply all migrations
    command.upgrade(alembic_cfg, "head")
