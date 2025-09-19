from pydantic import BaseModel
from typing import Optional

class MeetingRequest(BaseModel):
    meeting_url: str
    duration_minutes: Optional[int] = 30
    folder_name: Optional[str] = "Meeting Recordings"

class MeetingResponse(BaseModel):
    status: str
    message: str
    meeting_url: str
    duration_minutes: int
    recording_file: Optional[str] = None
    drive_link: Optional[str] = None
