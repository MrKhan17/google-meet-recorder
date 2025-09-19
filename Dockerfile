# Base image with Chrome + Selenium preinstalled
FROM selenium/standalone-chromium

# Switch to root
USER root
WORKDIR /app

# Install Python + ffmpeg + audio deps
RUN apt-get update && apt-get install -y \
    python3 python3-pip ffmpeg pulseaudio alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Symlink python/pip
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Recordings directory
RUN mkdir -p /app/recordings && chown -R seluser:seluser /app

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK CMD curl -f http://localhost:8000/ || exit 1

# Switch back to Selenium's default user
USER seluser

# Run app with uvicorn
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
