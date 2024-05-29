# import etl.scripts.api_import_requests as api_import_requests
# import etl.scripts.dw_tables as dw_tables
# import etl.scripts.kpi_views as kpi_views

# def main():
#     print("Starting ETL process...")

#     print("Running API import requests...")
#     api_import_requests.main()

#     print("Running data warehouse table processing...")
#     dw_tables.main()

#     print("Running KPI views processing...")
#     kpi_views.main()

#     print("ETL process completed successfully!")

# if __name__ == "__main__":
#     main()

import logging.config
import json
import os

import etl.scripts.api_import_requests as api_import_requests
import etl.scripts.dw_tables as dw_tables
import etl.scripts.kpi_views as kpi_views


# Create logs directory if it doesn't exist
# if not os.path.exists('logs'):
#     os.makedirs('logs')

# Load logging configuration from JSON file
with open('/app/etl/logging_config.json', 'r') as f:
    config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

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
        logger.error("An error occurred during the ETL process", exc_info=True)

if __name__ == "__main__":
    main()
