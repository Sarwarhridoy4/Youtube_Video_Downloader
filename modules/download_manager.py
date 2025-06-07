# modules/download_manager.py
import os
import shutil
from yt_dlp import YoutubeDL

def download_video_with_progress(url, quality, dest, progress_hook):
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        raise FileNotFoundError("FFmpeg not found. Please install FFmpeg and ensure it's in your PATH.")

    ydl_opts = {
        'format': quality or 'best',
        'outtmpl': os.path.join(dest, '%(title).70s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'progress_hooks': [progress_hook],
        'merge_output_format': 'mp4',
        'ffmpeg_location': ffmpeg_path,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
