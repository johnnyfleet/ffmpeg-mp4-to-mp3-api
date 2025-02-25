from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
import subprocess
import os
import uuid
import time
import threading

app = FastAPI(
    title="FFmpeg MP4 to MP3 API",
    description="API to convert MP4 to MP3 using FFmpeg with auto cleanup.",
    version="1.1.2",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

UPLOAD_FOLDER = "/data"

def delete_file_after_delay(file_path: str, delay: int = 600):  # Default: 24 hours (86400s)
    """Deletes a file after a given delay (default: 24 hours)."""
    time.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")

@app.post("/convert", summary="Convert MP4 to MP3", tags=["Conversion"])
async def convert_mp4_to_mp3(file: UploadFile = File(...)):
    """
    Upload an MP4 file and convert it to MP3 using FFmpeg.
    The original MP4 file is deleted after conversion.
    """
    file_id = str(uuid.uuid4())
    mp4_path = f"{UPLOAD_FOLDER}/{file_id}.mp4"
    mp3_path = f"{UPLOAD_FOLDER}/{file_id}.mp3"

    # Save uploaded file
    with open(mp4_path, "wb") as buffer:
        buffer.write(await file.read())

    # Run FFmpeg conversion
    command = ["ffmpeg", "-i", mp4_path, "-q:a", "0", "-map", "a", mp3_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Delete the original MP4 file (cleanup)
    if os.path.exists(mp4_path):
        os.remove(mp4_path)
        print(f"Deleted MP4: {mp4_path}")

    # Check if conversion was successful
    if result.returncode == 0 and os.path.exists(mp3_path):
        return {"mp3_url": f"http://localhost:8000/download/{file_id}.mp3"}
    else:
        # Ensure MP3 is not left behind if conversion fails
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        return {"error": "Conversion failed"}

@app.get("/download/{filename}", summary="Download converted MP3", tags=["Download"])
async def download_file(filename: str, background_tasks: BackgroundTasks):
    """
    Download the converted MP3 file. The file is deleted after 24 hours.
    """
    file_path = f"{UPLOAD_FOLDER}/{filename}"

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    # Schedule file deletion after 24 hours
    background_tasks.add_task(delete_file_after_delay, file_path)

    return FileResponse(file_path, media_type="audio/mpeg", filename=filename)
