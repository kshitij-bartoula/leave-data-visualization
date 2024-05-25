#!/bin/sh

echo "my cronjob is working!"

# Run api_import_requests.py
python /app/etl/api_import_requests.py

#Run dw_tables.py
#python /app/etl/dw_tables.py

#Run kpi_views.py
#python /app/etl/kpi_views.py