
from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic Config object reads alembic.ini
config = context.config

# override the URL from settings.py → .env
from app.config import settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# set up python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# import SQLModel models so that SQLModel.metadata is populated
from sqlmodel import SQLModel
import app.auth.models       # defines User, BlacklistedToken
import app.predict.models    # defines Prediction

# use the SQLModel metadata for 'autogenerate'
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
