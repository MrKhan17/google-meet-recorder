# Google Meet Recording API

A FastAPI-based application that records Google Meet sessions and uploads them to Google Drive using Docker with Selenium.

## Quick Start

```bash
# 1. Clone and navigate to the project
cd /path/to/google_meet_recording

# 2. Copy environment file and configure
cp .env.example .env
# Edit .env with your Gmail credentials

# 3. Add your Google Drive API credentials
# Place your OAuth2 credentials.json file in the project root

# 4. Build and run
docker-compose up --build

# 5. Test the API
curl http://localhost:8000/
# Visit http://localhost:8000/docs for interactive API documentation
```

## Features

- 🎥 Automated Google Meet session recording
- 🔐 Google OAuth2 authentication for Drive access
- 🔄 Automatic login to Google accounts
- 📁 Upload recordings to Google Drive with organized folders
- 🐳 Fully containerized with Docker using Selenium
- 🔧 Built on Selenium standalone Chromium image
- 📊 Health checks and monitoring
- 🎛️ RESTful API interface with FastAPI
- 🎵 High-quality audio recording with FFmpeg
- 🖥️ VNC access for debugging and monitoring

## Prerequisites

- Docker and Docker Compose installed
- Google Account with access to Google Meet
- Google Drive API credentials (OAuth2)
- Gmail account credentials

### Key Dependencies

The application uses these main Python packages:
- **FastAPI**: Modern web framework for building APIs
- **Selenium**: Web browser automation
- **Google API Client**: Google Drive integration
- **FFmpeg**: Audio recording (installed in Docker container)
- **Uvicorn**: ASGI server for FastAPI
- **Pydantic**: Data validation and settings management

## Setup

### 1. Clone the repository and navigate to the project directory

```bash
cd /path/to/google_meet_recording
```

### 2. Set up environment variables

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:

```env
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
```

### 3. Set up Google Drive API credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Drive API
4. Create OAuth 2.0 credentials
5. Download the credentials and save as `credentials.json` in the project root

### 4. Build and run the application

```bash
# Build and start the application with Docker Compose
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

## Usage

### API Endpoints

The application provides the following endpoints:

- `GET /` - Health check
- `GET /docs` - API documentation (Swagger UI)
- `POST /record-meeting` - Start recording a meeting

### Recording a Meeting

Send a POST request to `/record-meeting`:

```bash
curl -X POST "http://localhost:8000/record-meeting" \
     -H "Content-Type: application/json" \
     -d '{
       "meeting_url": "https://meet.google.com/your-meeting-id",
       "duration_minutes": 30,
       "folder_name": "Meeting Recordings"
     }'
```

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Docker Services

### Main Service: google-meet-recorder

- **Base Image**: `selenium/standalone-chromium`
- **Ports**: 8000 (API), 4444 (Selenium), 7900 (VNC for debugging)
- **Features**: 
  - Python 3.11
  - FFmpeg for audio recording
  - Selenium WebDriver with Chromium
  - FastAPI application

## Management Commands

### Docker Compose Commands

```bash
# Start the services
docker-compose up -d

# Stop the services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up --build

# Check service status
docker-compose ps

# Access container shell
docker-compose exec google-meet-recorder /bin/bash
```

## Examples

### Start the application
```bash
docker-compose up -d
```

### Check if everything is working
```bash
# Check container status
docker-compose ps

# Test API health
curl http://localhost:8000/

# View API documentation
curl http://localhost:8000/docs
```

### Monitor logs
```bash
docker-compose logs -f
```

### Debug inside container
```bash
docker-compose exec google-meet-recorder /bin/bash
```

### Stop the application
```bash
docker-compose down
```

## Troubleshooting

### 1. Container fails to start
```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs google-meet-recorder
```

### 2. Chrome/Selenium issues
```bash
# Access container and test browser
docker-compose exec google-meet-recorder /bin/bash
chromium-browser --version

# Test Selenium WebDriver
python -c "from selenium import webdriver; from config import get_chrome_options; driver = webdriver.Chrome(options=get_chrome_options()); print('Selenium working'); driver.quit()"
```

### 3. API not responding
```bash
# Test API endpoints
curl http://localhost:8000/
curl http://localhost:8000/docs

# Check container health
docker-compose ps
```

### 4. Recording issues
- Ensure FFmpeg is installed in container: `docker-compose exec google-meet-recorder ffmpeg -version`
- Check audio devices: `docker-compose exec google-meet-recorder pactl list sources`
- Verify meeting URL is accessible
- Check microphone permissions in browser

### 5. Upload issues
- Verify Google Drive credentials in `credentials.json`
- Check if `token.pickle` file exists and is valid
- Ensure proper folder permissions
- Test OAuth flow manually

## Development

### Development Mode

For development with auto-reload, you can mount the source code as a volume:

```bash
# Add volume mount for development
docker-compose up --build
```

You can also run the FastAPI application directly on your host machine:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application with auto-reload
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Debugging

1. **VNC Access**: Connect to `localhost:7900` with VNC client (password: `secret`)
2. **Shell Access**: Use `docker-compose exec google-meet-recorder /bin/bash` for interactive debugging
3. **Logs**: Monitor with `docker-compose logs -f`
4. **API Testing**: Visit `http://localhost:8000/docs` for interactive API testing

## File Structure

```
├── app.py                        # Main FastAPI application
├── config.py                     # Configuration and Chrome options
├── models.py                     # Pydantic models for API requests/responses
├── google_meet.py                # Google Meet automation and recording logic
├── recording.py                  # FFmpeg audio recording functionality
├── google_drive_oauth.py         # Google Drive OAuth2 authentication
├── google_drive_service_account.py # Service account authentication (alternative)
├── google_drive_uploader (1).py  # Google Drive upload utilities
├── credentials.json              # Google API credentials (OAuth2)
├── token.pickle                  # OAuth token cache (auto-generated)
├── requirements.txt              # Python dependencies
├── .env                         # Environment variables (create from .env.example)
├── .env.example                 # Environment variables template
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker services configuration
├── .dockerignore               # Docker ignore patterns
├── .gitignore                  # Git ignore patterns
└── recordings/                 # Recording output directory (auto-created)
```

## Security Notes

- The application runs with restricted user permissions
- Credentials are handled via environment variables
- Network access is limited to required services
- Container uses security options for safe operation

## Performance

- **Memory**: 1-3GB recommended
- **CPU**: 0.5-2 cores depending on load
- **Storage**: Ensure sufficient space for recordings
- **Network**: Stable internet connection required

## License

This project is provided as-is for educational and development purposes.
