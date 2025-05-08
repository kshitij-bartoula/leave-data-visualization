FROM python:3.10.4-alpine

RUN apk update && apk upgrade && apk add --no-cache build-base

WORKDIR /app
COPY src/etl/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

ENV PYTHONPATH=/app/

CMD ["python", "/app/etl/scheduler.py"]
