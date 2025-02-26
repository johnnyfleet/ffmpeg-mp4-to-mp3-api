# FFmpeg API - Convert MP4 to MP3

[![Build and Push Docker Image](https://github.com/johnnyfleet/ffmpeg-mp4-to-mp3-api/actions/workflows/docker-build.yaml/badge.svg?branch=main)](https://github.com/johnnyfleet/ffmpeg-mp4-to-mp3-api/actions/workflows/docker-build.yaml)
[![Rebuild Docker Image on Base Image Update](https://github.com/johnnyfleet/ffmpeg-mp4-to-mp3-api/actions/workflows/docker-rebuild-on-upstream.yaml/badge.svg)](https://github.com/johnnyfleet/ffmpeg-mp4-to-mp3-api/actions/workflows/docker-rebuild-on-upstream.yaml)

A FastAPI-based microservice that converts **MP4 video files to MP3 audio files** using **FFmpeg**.
Automatically cleans up files and is designed for **Docker deployment** with **GitHub Actions CI/CD**.

## 🚀 Features
- **Convert MP4 to MP3** via REST API.
- **Automatic cleanup** of MP4 and MP3 files.
- **Swagger UI** and **ReDoc** documentation.
- **Dockerized** with GitHub Actions CI/CD.
- **Auto-rebuilds when base image (`python:3.10-alpine`) updates.**

## 🛠 Installation

### Run Locally (Docker)
```bash
docker run -d --name ffmpeg-mp4-to-mp3-api -p 8000:8000 \
  -v $(pwd):/data ghcr.io/johnnyfleet/ffmpeg-mp4-to-mp3-api:latest
```

## 📖 API Documentation

Once the service is running, you can access the following endpoints:

- **API Endpoint**: `http://localhost:8000/convert` - Use this endpoint to convert MP4 files to MP3.
- **Swagger UI**: `http://localhost:8000/docs` - Interactive API documentation and testing interface.
- **ReDoc**: `http://localhost:8000/redoc` - Alternative API documentation interface.
