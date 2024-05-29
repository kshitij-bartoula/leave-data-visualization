import etl.scripts.api_import_requests as api_import_requests
import etl.scripts.dw_tables as dw_tables
import etl.scripts.kpi_views as kpi_views

def main():
    print("Starting ETL process...")

    print("Running API import requests...")
    api_import_requests.main()

    print("Running data warehouse table processing...")
    dw_tables.main()

    print("Running KPI views processing...")
    kpi_views.main()

    print("ETL process completed successfully!")

if __name__ == "__main__":
    main()
