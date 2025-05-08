import schedule
import time
import etl.main as etl_main
import logging

logger = logging.getLogger(__name__)

def run_etl_job():
    logger.info(f"Running scheduled ETL job...")
    etl_main.main()

schedule.every(2).minutes.do(run_etl_job)

if __name__ == "__main__":
    logger.info(f"ETL Scheduler started. Running every 2 minutes.")
    run_etl_job()  # Run once immediately
    while True:
        schedule.run_pending()
        time.sleep(1)
