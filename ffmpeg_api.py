from fastapi import FastAPI, File, UploadFile
import subprocess
import os
import uuid

app = FastAPI(
    title="FFmpeg API",
    description="A FastAPI-based service to convert MP4 to MP3 using FFmpeg with GPU acceleration if available.",
    version="1.1.1",
)

UPLOAD_FOLDER = "/data"

def is_nvidia_available():
    """Check if an NVIDIA GPU is available using nvidia-smi."""
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0  # Returns True if GPU is found, False otherwise
    except FileNotFoundError:
        return False  # nvidia-smi command not found, so no GPU is available

@app.post("/convert", summary="Convert MP4 to MP3")
async def convert_mp4_to_mp3(file: UploadFile = File(...)):
    """
    Upload an MP4 file and convert it to MP3 using FFmpeg.
    Automatically uses NVIDIA GPU if available, otherwise falls back to CPU.
    """
    file_id = str(uuid.uuid4())
    mp4_path = f"{UPLOAD_FOLDER}/{file_id}.mp4"
    mp3_path = f"{UPLOAD_FOLDER}/{file_id}.mp3"

    # Save uploaded file
    with open(mp4_path, "wb") as buffer:
        buffer.write(await file.read())

    # Determine if GPU is available
    use_gpu = is_nvidia_available()

    # Define FFmpeg command
    if use_gpu:
        print("✅ NVIDIA GPU detected! Using hardware acceleration.")
        command = [
            "ffmpeg",
            "-hwaccel", "cuda",  # Enable CUDA acceleration
            "-i", mp4_path,
            "-c:a", "aac",  # Use GPU-accelerated audio encoding
            "-b:a", "192k",
            "-map", "a",
            mp3_path
        ]
    else:
        print("⚠ No NVIDIA GPU detected. Using CPU for conversion.")
        command = [
            "ffmpeg",
            "-i", mp4_path,
            "-q:a", "0",
            "-map", "a",
            mp3_path
        ]

    # Run FFmpeg
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Cleanup MP4 file
    if os.path.exists(mp4_path):
        os.remove(mp4_path)
        print(f"🗑 Deleted MP4 file: {mp4_path}")

    # Check if conversion was successful
    if result.returncode == 0 and os.path.exists(mp3_path):
        return {"mp3_url": f"http://localhost:8000/download/{file_id}.mp3"}
    else:
        # Cleanup MP3 file if conversion failed
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        return {"error": "Conversion failed"}
