# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Update OS packages to fix vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libxslt1-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
