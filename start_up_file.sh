#!/bin/sh

echo "my cronjob is working!"

# Run etl
python /app/etl/etl_main.py

#Run dw_tables.py
#python /app/etl/dw_tables.py

#Run kpi_views.py
#python /app/etl/kpi_views.py