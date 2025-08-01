# Use official Python 3.11+ image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Make simpleops-cli executable
RUN chmod +x simpleops-cli

# Optional: Set AWS CLI (useful for debugging)
# RUN pip install awscli

# Run the tool
CMD ["python", "simpleops-cli"]
