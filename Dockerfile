FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app

# Install system dependencies (correct apt usage + cleanup)
RUN apt-get update && apt-get install -y awscli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "app.py"]
