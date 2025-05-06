FROM python:3.10.4-alpine
RUN apk update && apk upgrade

# Install system dependencies required for PostgreSQL and other packages
RUN apk add --no-cache \
    build-base \
    dcron

WORKDIR /app
COPY src/etl/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

# Copy the cron configuration file into the container
COPY src/etl/cronfile /etc/cron.d/my-cron-job

RUN chmod 0644 /etc/cron.d/my-cron-job

# Copy the start_up_file.sh script into the container
COPY src/etl/start_up_file.sh /start_up_file.sh

RUN chmod +x /start_up_file.sh

RUN echo -e "*/2 * * * * /start_up_file.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron-job

RUN touch /var/log/cron.log

ENV PYTHONPATH=/app/

# Create a shell script to start both cron daemon and log tailing
RUN echo -e '#!/bin/sh\ntail -f /var/log/cron.log &\ncrond -f -d 8' > /start_services.sh

RUN chmod +x /start_services.sh

ENTRYPOINT ["/start_services.sh"]
