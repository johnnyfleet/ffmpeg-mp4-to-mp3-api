# Use a minimal Alpine-based Python image
FROM python:3.10-alpine

# Install FFmpeg and other dependencies
RUN apk add --no-cache ffmpeg bash

# Set working directory
WORKDIR /app

# Copy dependencies first (better Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose API port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "ffmpeg_api:app", "--host", "0.0.0.0", "--port", "8000"]

