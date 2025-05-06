FROM python:3.10.4-alpine
RUN apk update && apk upgrade

WORKDIR /app
COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .
ENV PYTHONPATH=/app/

EXPOSE 8000

COPY src/backend .
CMD ["python", "main.py"]
