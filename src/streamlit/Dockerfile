# Use Python 3.12 for better compatibility
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY src/streamlit/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY src/streamlit .

# Set environment variable
ENV PYTHONPATH=/app/

# Expose custom Streamlit port (default is 8501)
EXPOSE 8502

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]
