#!/bin/sh

echo "my cronjob is working!"

# Run etl
python /app/etl/etl_main.py
