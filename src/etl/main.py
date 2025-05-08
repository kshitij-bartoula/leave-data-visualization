import logging.config, json, os, smtplib
from email.mime.text import MIMEText
from sqlalchemy import text

import etl.scripts.api_ingestion as api_ingestion
import etl.scripts.dw_tables as dw_tables
import etl.scripts.dbo_tables as dbo_tables
import etl.scripts.kpi_views as kpi_views
from utils.db_utils import connection

# Load logging config
try:
    with open('/app/etl/logging_config.json', 'r') as f:
        logging.config.dictConfig(json.load(f))
except Exception:
    raise RuntimeError("Logging config failed to load")

logger = logging.getLogger(__name__)

def send_failure_email(error_message):
    try:
        to, sender, password = os.getenv('RECIPIENT_EMAIL'), os.getenv('SENDER_EMAIL'), os.getenv('SENDER_DATA')
        if not all([to, sender, password]):
            return

        msg = MIMEText(f"The ETL process failed:\n\n{error_message}")
        msg['Subject'], msg['From'], msg['To'] = "ETL Process Failure", sender, to

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, to, msg.as_string())
        logger.info("Failure email sent successfully")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred ,Failed to send failure email: {e}")

def fetch_config_flags(db_engine):
    query = text("""
        SELECT is_ingestion_enabled, is_transformation_enabled
        FROM config.import_config
        WHERE api_name = :api_name
    """)
    with db_engine.connect() as conn:
        result = conn.execute(query, {"api_name": "vyaguta"}).fetchone()
        return dict(result._mapping) if result else None

def update_config_flag(db_engine, column, value):
    query = text(f"""
        UPDATE config.import_config
        SET {column} = :value
        WHERE api_name = :api_name
    """)
    with db_engine.begin() as conn:
        conn.execute(query, {"value": value, "api_name": "vyaguta"})
    logger.info(f"{column} disabled due to failure.")

def main():
    logger.info("ETL started.")
    db_engine = connection()

    try:
        flags = fetch_config_flags(db_engine)
        if not flags:
            raise ValueError("Missing config flags for 'vyaguta'")

        if flags.get("is_ingestion_enabled"):
            logger.info("Running ingestion.")
            try:
                api_ingestion.main()
                logger.info("ingestion completed.")
            except Exception as e:
                logger.info("Disabling ingestion due to failure.")
                update_config_flag(db_engine, "is_ingestion_enabled", False)
                send_failure_email(f"Ingestion failed:\n{e}")
        else:
            logger.info("Ingestion is disabled.")


        if flags.get("is_transformation_enabled"):
            logger.info("Running transformations.")
            try:
                dbo_tables.main()
                logger.info("cleaned data moved to dbo tables completed.")
                dw_tables.main()
                kpi_views.main()
                logger.info("transformations completed.")
            except Exception as e:
                logger.info("Disabling transformation due to failure.")
                update_config_flag(db_engine, "is_transformation_enabled", False)
                send_failure_email(f"Transformation failed:\n{e}")
        else:
            logger.info("Transformation is disabled.") 

    except Exception as e:
        logger.error("ETL process failed", exc_info=True)
        send_failure_email(str(e))
        raise

if __name__ == "__main__":
    main()
