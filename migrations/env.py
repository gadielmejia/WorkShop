import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

from src.app import Base  # noqa: F401
from src.app import app as _app  # noqa: F401,F811

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Add our source directory to the path so we can import the app's Base
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()
