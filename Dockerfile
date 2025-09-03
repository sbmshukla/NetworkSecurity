FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app

# Install system dependencies
RUN apt  update -y && apt  install awscli -y

# Install Python dependencies
RUN apt-get update && pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "app.py"]
