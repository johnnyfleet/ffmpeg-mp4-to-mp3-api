# Use a minimal Python + Alpine base image
FROM python:3-alpine

# Set default PUID and PGID for Unraid (can be overridden)
ARG PUID=99
ARG PGID=100

# Install FFmpeg and dependencies
RUN apk add --no-cache ffmpeg bash \
    # Ensure the group exists
    && if ! getent group $PGID >/dev/null; then addgroup -g $PGID appgroup; else groupname=$(getent group $PGID | cut -d: -f1); fi \
    # Ensure the user exists and assign to the correct group
    && if ! getent passwd $PUID >/dev/null; then adduser -D -G "${groupname:-appgroup}" -u $PUID appuser; fi

# Set the working directory
WORKDIR /app

# Copy dependencies first to optimize Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Ensure the correct ownership of files for the Unraid user
RUN chown -R $PUID:$PGID /app

# Switch to the non-root user
USER $PUID

# Expose the API port
EXPOSE 8000

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "ffmpeg_api:app", "--host", "0.0.0.0", "--port", "8000"]
