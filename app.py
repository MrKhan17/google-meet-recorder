#!/usr/bin/env python3
"""
FastAPI application for Google Meet recording
Provides API endpoints to start and manage Google Meet recordings
"""

import uvicorn
import config

from fastapi import FastAPI, HTTPException

from google_meet import record_meeting

from models import MeetingRequest, MeetingResponse

logger = config.get_logger()

app = FastAPI(
    title="Google Meet Recording API",
    description="API for recording Google Meet sessions and uploading to Google Drive",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Google Meet Recording API",
        "status": "running",
        "version": "1.0.0"
    }

@app.post("/record-meeting", response_model=MeetingResponse)
async def record_meeting_endpoint(request: MeetingRequest):
    """Record a Google Meet session and upload to Google Drive"""
    try:
        # Validate
        duration_minutes = request.duration_minutes or 30
        folder_name = request.folder_name or "Meeting Recordings"
        
        # Record the meeting
        result = await record_meeting(request.meeting_url, duration_minutes, folder_name)

        if result["success"]:
            return MeetingResponse(
                status="completed",
                message=result["message"],
                meeting_url=request.meeting_url,
                duration_minutes=duration_minutes,
                recording_file=result["recording_file"],
                drive_link=result["drive_link"]
            )
        else:
            return MeetingResponse(
                status="failed",
                message=result["message"],
                meeting_url=request.meeting_url,
                duration_minutes=duration_minutes,
                recording_file=result["recording_file"],
                drive_link=result["drive_link"]
            )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid meeting URL: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to record meeting: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to record meeting: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
