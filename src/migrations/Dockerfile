# Use a specific version of the Python image for consistency
FROM python:3.9-slim

WORKDIR /app
COPY src/migrations/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .
ENV PYTHONPATH=/app/

# Copy the application code including SQL files
COPY src/migrations .

CMD ["python", "migration.py"]
