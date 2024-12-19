FROM python:3.9-slim

# Install libicu and Python dependencies
RUN apt-get update && apt-get install -y \
    libicu-dev && \
    apt-get clean

# Set up your app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# Run the app
CMD ["python", "app.py"]
