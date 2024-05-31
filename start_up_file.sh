#!/bin/sh

echo "my cronjob is working!"

# Run etl
python /app/etl/etl_main.py

echo "api.py is executing"
python /app/app/scripts/api.py
echo "api.py is execution complete"

#Run dw_tables.py
#python /app/etl/dw_tables.py

#Run kpi_views.py
#python /app/etl/kpi_views.py