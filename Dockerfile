# Use Python 3.12.5 from the official Docker Hub
FROM python:3.12.5-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY . /app
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
