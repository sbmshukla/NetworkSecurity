FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app

# Install system dependencies and clean up APT cache
RUN apt-get update && apt-get install -y awscli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN apt-get update && pip install -r requirements.txt

# Run the application
CMD ["python", "app.py"]
