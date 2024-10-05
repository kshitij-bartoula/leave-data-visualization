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

import etl.scripts.api_import_requests as api_import_requests
import etl.scripts.dw_tables as dw_tables
import etl.scripts.kpi_views as kpi_views


# Load logging configuration from JSON file
with open('/app/etl/logging_config.json', 'r') as f:
    config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

def send_failure_email(error_message):
    """Send email notification when ETL process fails."""
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_DATA')

    print(f"Sender Email: {sender_email}")
    print(f"Recipient Email: {recipient_email}") 

    msg = MIMEText(f"The ETL process failed with the following error:\n\n{error_message}")
    msg['Subject'] = "ETL Process Failure Notification"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        # Setup SMTP server connection
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        logger.info("Failure notification email sent successfully.")
    except Exception as e:
        logger.error("Failed to send failure notification email", exc_info=True)

def main():
    logger.info("Starting ETL process...")

    try:
        logger.info("Running API import requests...")
        api_import_requests.main()

        logger.info("Running data warehouse table processing...")
        dw_tables.main()

        logger.info("Running KPI views processing...")
        kpi_views.main()

        logger.info("ETL process completed successfully!")
    except Exception as e:
        error_message = str(e)
        logger.error("An error occurred during the ETL process", exc_info=True)
        send_failure_email(error_message)

if __name__ == "__main__":
    main()
