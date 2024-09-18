import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# Alembic Config object, which provides access to values within the .ini file
config = context.config

# Set up loggers as per alembic.ini
fileConfig(config.config_file_name)

# MetaData object, you can set this to support 'autogenerate' if needed.
target_metadata = None

# Path to the folder with the SQL migration scripts
SQL_FOLDER = 'sql'


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection)

        # Start a transaction
        with context.begin_transaction():
            # Get a list of all SQL files in the 'sql' folder and sort them
            sql_files = sorted([f for f in os.listdir(SQL_FOLDER) if f.endswith('.sql')])

            for sql_file in sql_files:
                sql_path = os.path.join(SQL_FOLDER, sql_file)

                # Read and execute each SQL file
                with open(sql_path, 'r') as file:
                    sql_command = file.read()
                    print(f"Running SQL migration: {sql_file}")
                    connection.execute(sql_command)

            # Run any additional Alembic-specific migrations (if needed)
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
