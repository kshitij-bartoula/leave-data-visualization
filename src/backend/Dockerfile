FROM python:3.10.4-alpine
RUN apk update && apk upgrade

# Install system dependencies required for PostgreSQL and other packages
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
COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .
ENV PYTHONPATH=/app/

EXPOSE 8000

COPY src/backend .
CMD ["python", "main.py"]
