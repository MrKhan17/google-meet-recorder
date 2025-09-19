import asyncio
import os

async def start_recording_async(output_file: str, duration_seconds: int, pulse_source: str = "default"):
    """Start FFmpeg recording asynchronously"""
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "pulse", 
        "-i", pulse_source,
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_file
    ]
    
    print(f"Starting recording: {' '.join(cmd)}")
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    try:
        await asyncio.sleep(duration_seconds)
    finally:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=10)
        except asyncio.TimeoutError:
            process.kill()
    
    return os.path.exists(output_file)
