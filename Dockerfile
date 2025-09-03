FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app

# Install system dependencies and clean up APT cache
RUN apt-get update && apt-get install -y awscli \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "app.py"]

