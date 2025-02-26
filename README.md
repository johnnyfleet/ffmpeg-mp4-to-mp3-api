# FFmpeg API - Convert MP4 to MP3

[![Build and Push Docker Image](https://github.com/johnnyfleet/ffmpeg-mp4-to-mp3-api/actions/workflows/docker-build.yaml/badge.svg?branch=main)](https://github.com/johnnyfleet/ffmpeg-mp4-to-mp3-api/actions/workflows/docker-build.yaml)
[![Rebuild Docker Image on Base Image Update](https://github.com/johnnyfleet/ffmpeg-mp4-to-mp3-api/actions/workflows/docker-rebuild-on-upstream.yaml/badge.svg)](https://github.com/johnnyfleet/ffmpeg-mp4-to-mp3-api/actions/workflows/docker-rebuild-on-upstream.yaml)

A FastAPI-based microservice that converts **MP4 video files to MP3 audio files** using **FFmpeg**.
Designed for **Unraid**, with optional **NVIDIA GPU acceleration** for faster conversion.

## 🚀 Features
- **Convert MP4 to MP3** via REST API.
- **Automatic cleanup** of MP4 and MP3 files.
- **Detects and uses NVIDIA GPU if available** (falls back to CPU if not).
- **Customizable port and storage path** via Unraid's UI.
- **Dockerized with GitHub Actions CI/CD**.
- **Auto-rebuilds when base image (`python:3.10-alpine`) updates.**

## 🛠 Installation

### **Option 1️⃣: Run with Docker Locally**
1. **Build and run the container:**
   ```bash
   docker run -p 8000:8000 -v $(pwd)/data:/data ghcr.io/johnnyfleet/ffmpeg-mp4-to-mp3-api:latest
   ```
2. The API will now be available at:
   **[http://localhost:8000](http://localhost:8000)**

### **Option 2️⃣: Install via Unraid Web UI**
1. Go to **Unraid Web UI** → `Docker` → **Add Container**.
2. Select **"FFmpeg API"** from the **template dropdown**.
3. Customize the following:
   - **Data Path (`DATA_PATH`)** → Choose where MP3 files are stored.
   - **Port (`WEB_PORT`)** → Default is `8000`, but you can change it.
   - **User ID (`PUID`)** → Set to `99` (default Unraid user).
   - **Group ID (`PGID`)** → Set to `100` (default Unraid group).
   - *(Optional)* **NVIDIA GPU Support** – Set `NVIDIA_VISIBLE_DEVICES=all` if using an NVIDIA GPU.
4. Click **Apply** to deploy the container.

## 📱 Documentation

Comes with swagger and redoc as part of FastAPI.

You can access swagger via **[http://localhost:8000/docs](http://localhost:8000/docs)**

## 💪 NVIDIA GPU Acceleration (Optional)
If you have an **NVIDIA GPU**, you can use it to **speed up MP4 to MP3 conversion**.

### 1️⃣ Install NVIDIA Drivers
#### On Unraid
1. Go to **Unraid Web UI** → `Apps` tab.
2. Search for **"NVIDIA Driver"** (by Unraid) and install it.
3. Reboot the server.
4. Check if Unraid detects the GPU:
   ```bash
   nvidia-smi
   ```

#### On a Local Machine
1. Install **NVIDIA Container Toolkit**:
   ```bash
   sudo apt update && sudo apt install -y nvidia-container-toolkit
   ```
2. Restart Docker:
   ```bash
   sudo systemctl restart docker
   ```

### ****2️⃣ Enable GPU for FFmpeg API****
#### On Unraid
1. **Set `NVIDIA_VISIBLE_DEVICES=all`** in the template.
2. **Deploy the container**.

#### On a Local Machine
1. **Run the container with GPU support:**
   ```bash
   docker run -d --gpus all --name ffmpeg-api -p 8000:8000 \
     -v $(pwd)/data:/data \
     -e PUID=99 -e PGID=100 \
     -e NVIDIA_VISIBLE_DEVICES=all \
     ffmpeg-api
   ```

### 3️⃣ Verify GPU is Used
Run inside the container:
```bash
docker exec -it ffmpeg-api ffmpeg -hwaccels
```
If you see **CUDA or NVENC listed**, the GPU is being used.

## 🔍 License
This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for details.