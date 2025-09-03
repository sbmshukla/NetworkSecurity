FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app

# Install system dependencies and clean up APT cache
RUN apt update -y && apt install awscli -y

# Install Python dependencies
RUN apt-get update && pip install -r requirements.txt

# Run the application
CMD ["python", "app.py"]