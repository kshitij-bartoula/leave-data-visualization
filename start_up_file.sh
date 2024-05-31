#!/bin/sh

echo "my cronjob is working!"

# Run etl
python /app/etl/etl_main.py

echo "db conection executing!"
python /app/scripts/database.py

echo "api.py executing!"
python app/scripts/api.py
echo "api.py executed!"

#Run dw_tables.py
#python /app/etl/dw_tables.py

#Run kpi_views.py
#python /app/etl/kpi_views.py