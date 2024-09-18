import os
from alembic import context
from sqlalchemy import create_engine, pool, text
from logging.config import fileConfig

# Alembic Config object, which provides access to values within the .ini file
config = context.config

# Set up loggers as per alembic.ini
fileConfig(config.config_file_name)

# MetaData object, you can set this to support 'autogenerate' if needed.
target_metadata = None

# Use the environment variable for SQLALCHEMY_DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Path to the folder with the SQL migration scripts
SQL_FOLDER = 'sql'


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = SQLALCHEMY_DATABASE_URL  # Use the URL from the environment
    context.configure(url=url, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Create engine using SQLALCHEMY_DATABASE_URL from the environment
    connectable = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection)

        # Ensure that the migration history table exists
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS migration_history (
                id SERIAL PRIMARY KEY,
                migration_name VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

        # Start a transaction
        with context.begin_transaction():
            # Get a list of all SQL files in the 'sql' folder and sort them
            sql_files = sorted([f for f in os.listdir(SQL_FOLDER) if f.endswith('.sql')])

            for sql_file in sql_files:
                # Check if this migration has already been applied
                result = connection.execute(
                    text("SELECT migration_name FROM migration_history WHERE migration_name = :name"),
                    {"name": sql_file}
                ).fetchone()

                if result:
                    print(f"Skipping already applied migration: {sql_file}")
                    continue  # Skip this migration as it has already been applied

                # Read and execute each SQL file
                sql_path = os.path.join(SQL_FOLDER, sql_file)
                with open(sql_path, 'r') as file:
                    sql_command = file.read()
                    print(f"Running new SQL migration: {sql_file}")
                    connection.execute(text(sql_command))

                # Record the migration in the migration_history table
                connection.execute(
                    text("INSERT INTO migration_history (migration_name) VALUES (:name)"),
                    {"name": sql_file}
                )

            # Run any additional Alembic-specific migrations (if needed)
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
