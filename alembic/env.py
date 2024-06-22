import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.engine import Connection
from sqlalchemy import pool

from alembic import context
from workout_api.contrib.models import BaseModel
#import de todo o DB da pasta repository onde constam apenas os imports (forma de manipular os dados de um local neltro)
from workout_api.contrib.repository.models import *
import os

# Load environment variables if using a .env file
from dotenv import load_dotenv
load_dotenv()

config = context.config

# Fetch the database URL from environment variables
DB_DRIVER = os.getenv('DB_DRIVER')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Construct the SQLAlchemy URL
sqlalchemy_url = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Update the config object with the constructed URL
config.set_main_option('sqlalchemy.url', sqlalchemy_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

#Estamos chamando a nossa BaseModel com a função metadata, agora vamos importar todo DB para que ele reconheça.
target_metadata = BaseModel.metadata

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

def do_run_migrations(connection: Connection) ->None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
