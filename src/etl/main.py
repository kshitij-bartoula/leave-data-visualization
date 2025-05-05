"""
Runs the ETL (Extract, Transform, Load) process for importing data from APIs, processing data warehouse tables, and generating KPI views.

Imports logging configuration, JSON, and necessary ETL scripts.

Functionality:
- Loads logging configuration from a JSON file.
- Configures logging using the loaded configuration.
- Defines a main function to orchestrate the ETL process.
- Executes API import requests, data warehouse table processing, and KPI views processing sequentially.
- Logs information and errors during the ETL process.

"""

import logging.config
import json
import os
import smtplib
from email.mime.text import MIMEText
from sqlalchemy import text

import etl.scripts.api_ingestion as api_ingestion
import etl.scripts.dw_tables as dw_tables
import etl.scripts.kpi_views as kpi_views

from utils.db_utils import connection

# Load logging configuration
with open('/app/etl/logging_config.json', 'r') as f:
    config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

def send_failure_email(error_message):
    """Send email notification when ETL process fails."""
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_DATA')

    msg = MIMEText(f"The ETL process failed with the following error:\n\n{error_message}")
    msg['Subject'] = "ETL Process Failure Notification"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        logger.info("Failure notification email sent successfully.")
    except Exception as e:
        logger.error("Failed to send failure notification email", exc_info=True)

def fetch_config_flags(db_engine):
    """Fetch ingestion and transformation flags from config.import_config"""
    query = text("SELECT is_ingestion_enabled, is_transformation_enabled FROM config.import_config WHERE api_name = 'vyaguta'")
    with db_engine.connect() as conn:
        result = conn.execute(query).fetchone()
        return dict(result._mapping) if result else None  # Use _mapping for SQLAlchemy Row

def update_config_flag(db_engine, column, value):
    """Update a single flag in config.import_config table"""
    update_query = text(f"""
        UPDATE config.import_config
        SET {column} = :value
        WHERE api_name = 'vyaguta'
    """)
    with db_engine.begin() as conn:
        conn.execute(update_query, {"value": value})

def main():
    logger.info("Starting ETL process...")
    db_engine = connection()

    try:
        config_flags = fetch_config_flags(db_engine)

        if not config_flags:
            raise ValueError("No configuration found for 'vyaguta' in config.import_config")

        # Run ingestion if enabled
        if config_flags["is_ingestion_enabled"]:
            try:
                logger.info("Ingestion_enabled status true..Running API ingestion step...")
                api_ingestion.main()
            except Exception as e:
                logger.error("API ingestion failed", exc_info=True)
                update_config_flag(db_engine, "is_ingestion_enabled", False)
                #send_failure_email(f"API Ingestion failed: {str(e)}")
                raise

        # Run transformation if enabled
        if config_flags["is_transformation_enabled"]:
            try:
                logger.info("Running data warehouse table processing...")
                dw_tables.main()

                logger.info("Running KPI views processing...")
                kpi_views.main()
            except Exception as e:
                logger.error("Transformation step failed", exc_info=True)
                update_config_flag(db_engine, "is_transformation_enabled", False)
                #send_failure_email(f"Transformation failed: {str(e)}")
                raise

        logger.info("ETL process completed successfully!")

    except Exception as e:
        logger.error("An error occurred during the ETL process", exc_info=True)
        #send_failure_email(f"ETL Process failed:\n{str(e)}")

if __name__ == "__main__":
    main()
