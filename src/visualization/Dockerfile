FROM python:3.10.4-alpine

RUN apk update && apk upgrade

RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    libpq \
    curl \
    libressl-dev \
    musl-dev \
    libffi-dev \
    openssl-dev \
    gcc \
    libc-dev

WORKDIR /app

COPY src/visualization/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/visualization .
EXPOSE 8050

CMD ["python", "app.py"]