# FFmpeg API - Convert MP4 to MP3

![GitHub Workflow Status](https://github.com/johnnyfleet/ffmpeg-mp4-to-mp3-api/actions/workflows/docker-build.yml/badge.svg)
![GitHub Workflow Status](https://github.com/johnnyfleet/ffmpeg-mp4-to-mp3-api/actions/workflows/docker-rebuild-on-upstream.yml/badge.svg)

A FastAPI-based microservice that converts **MP4 video files to MP3 audio files** using **FFmpeg**.
Automatically cleans up files and is designed for **Docker deployment** with **GitHub Actions CI/CD**.

---

## 🚀 Features
- **Convert MP4 to MP3** via REST API.
- **Automatic cleanup** of MP4 and MP3 files.
- **Swagger UI** and **ReDoc** documentation.
- **Dockerized** with GitHub Actions CI/CD.
- **Auto-rebuilds when base image (`python:3.10-alpine`) updates.**

---

## 🛠 Installation

### 1️⃣ **Run Locally (Docker)**
```bash
docker run -d --name ffmpeg-mp4-to-mp3-api -p 8000:8000 \
  -v /path/to/data:/data ghcr.io/johnnyfleet/ffmpeg-mp4-to-mp3-api:latest
